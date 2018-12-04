# Daniel Peek qer419
# Michael Canas ohh135
# CS 3793 Final Project
# 12/4/18

import nltk
import gensim
import neural_net as nn
import random
import pickle
import argparse
import sys

total_guesses = 0
correct_guesses = 0


def main():
    parser = argparse.ArgumentParser(description='Train and test a neural network for part-of-speech tagging')
    parser.add_argument('-t', '--test', help='Select to test neural net, instead of training',
                        action='store_true', default=False)
    parser.add_argument('-i', '--input', help='File to read input from', default=None)
    parser.add_argument('-o', '--output', help='File to save output to', default=None)
    parser.add_argument('-e', '--epochs', help='number of epochs to train for', type=int, default=None)
    args = parser.parse_args()
    if args.test and args.input is None:
        parser.error('Testing mode requires a trained neural network input file')
    if args.test and args.output is not None:
        print('Output option is not active in testing mode', file=sys.stderr)
    if args.test and args.epochs is not None:
        print('Epochs are not used in testing mode', file=sys.stderr)

    nltk.download('averaged_perceptron_tagger')

    print('Loading Word2Vec model, please wait...')
    model = gensim.models.KeyedVectors.load_word2vec_format('trained-model.bin', binary=True)
    print('Word2Vec model loaded.')

    eta = .01
    neural_nets = None
    testing = args.test

    if args.epochs is not None:
        epochs = args.epochs
    else:
        epochs = 1000

    if args.input is not None:
        with open(args.input, 'rb') as input_file:
            neural_nets = pickle.load(input_file)

    if neural_nets is None:
        neural_nets = [nn.NeuralNetwork(eta) for __ in range(10)]
    with open('sentences') as file:
        sentences = [line.rstrip('\n.,').replace(' to ', ' ').replace(' and ', ' ')
                         .replace(' of ', ' ').replace('To ', '') for line in file]

    training_data = sentences[:650]
    testing_data = sentences[650:]

    if testing:
        for line in testing_data:
            run(line, model, neural_nets, 0, testing)
        pct = (correct_guesses / total_guesses) * 100.0
        print('%.04f%% correct\n' % pct)
        exit(0)

    else:
        for epoch in range(epochs):
            line = random.choice(training_data)
            run(line, model, neural_nets, epoch, testing)
            if epoch % 10000 == 0:
                if args.output is not None:
                    with open(args.output, 'wb') as output_file:
                        pickle.dump(neural_nets, output_file, -1)

    if args.output is not None and not testing:
        with open(args.output, 'wb') as output_file:
            pickle.dump(neural_nets, output_file, -1)
        exit(0)


def run(line, model, neural_nets, epoch, testing):
    global total_guesses
    global correct_guesses
    correct_ans = -1

    tokens = gensim.utils.simple_preprocess(line)
    tagged_line = nltk.pos_tag(tokens)
    tags = [pos for __, pos in tagged_line]

    for i in range(len(tags)):
        if tags[i].startswith('N'):
            tags[i] = 'noun'
        elif tags[i].startswith('V'):
            tags[i] = 'verb'
        elif tags[i].startswith('J'):
            tags[i] = 'adjective'
        elif tags[i].startswith('R'):
            tags[i] = 'adverb'
        elif tags[i].startswith('I'):
            tags[i] = 'preposition'
        else:
            tags[i] = 'unknown'

    vectors = [model[word] for word in tokens]
    for i in range(len(tokens)):
        guess = neural_nets[i].predict(vectors[i])

        if guess == 0:
            guess_pos = 'noun'
        elif guess == 1:
            guess_pos = 'verb'
        elif guess == 2:
            guess_pos = 'adjective'
        elif guess == 3:
            guess_pos = 'adverb'
        elif guess == 4:
            guess_pos = 'preposition'
        else:
            guess_pos = 'unknown'

        if not testing:
            if tags[i] == 'noun':
                correct_ans = 0
            elif tags[i] == 'verb':
                correct_ans = 1
            elif tags[i] == 'adjective':
                correct_ans = 2
            elif tags[i] == 'adverb':
                correct_ans = 3
            elif tags[i] == 'preposition':
                correct_ans = 4

        total_guesses += 1
        if guess_pos == tags[i]:
            correct_guesses += 1

        if not testing:
            neural_nets[i].adjust_weights(vectors[i], correct_ans)

    if epoch % 100 == 0 and not testing:
        print('epoch', epoch)
        pct = (correct_guesses / total_guesses) * 100.0
        print('%.04f%% correct\n' % pct)


if __name__ == '__main__':
    main()
