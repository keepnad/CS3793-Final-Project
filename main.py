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

# total and correct guesses made by the neural network
total_guesses = 0
correct_guesses = 0


# main function, handles arguments and neural net setup
def main():
    # argument parser
    parser = argparse.ArgumentParser(description='Train and test a neural network for part-of-speech tagging')
    parser.add_argument('-t', '--test', help='Select to test neural net, instead of training',
                        action='store_true', default=False)
    parser.add_argument('-i', '--input', help='File to read input from', default=None)
    parser.add_argument('-o', '--output', help='File to save output to', default=None)
    parser.add_argument('-e', '--epochs', help='number of epochs to train for', type=int, default=None)
    args = parser.parse_args()

    # argument errors and warnings
    if args.test and args.input is None:
        parser.error('Testing mode requires a trained neural network input file')
    if args.test and args.output is not None:
        print('Output option is not active in testing mode', file=sys.stderr)
    if args.test and args.epochs is not None:
        print('Epochs are not used in testing mode', file=sys.stderr)

    # install the needed nltk module, if not present
    nltk.download('averaged_perceptron_tagger')

    # load the Word2Vec model. This can take a little while, so added text to clarify
    print('Loading Word2Vec model, please wait...')
    model = gensim.models.KeyedVectors.load_word2vec_format('trained-model.bin', binary=True)
    print('Word2Vec model loaded.')

    # setup for neural network
    eta = .01
    neural_nets = None
    testing = args.test

    # set number of epochs if specified, else 1000
    if args.epochs is not None:
        epochs = args.epochs
    else:
        epochs = 1000

    # if neural net input file specified, open it and load it into the neural nets list
    if args.input is not None:
        with open(args.input, 'rb') as input_file:
            neural_nets = pickle.load(input_file)

    # else, create a new random-weighted list of 10 neural nets
    if neural_nets is None:
        neural_nets = [nn.NeuralNetwork(eta) for __ in range(10)]

    # open the sentence input file, remove some words we aren't classifying
    with open('sentences') as file:
        sentences = [line.rstrip('\n.,').replace(' to ', ' ').replace(' and ', ' ')
                         .replace(' of ', ' ').replace('To ', '') for line in file]

    # split sentences into training and testing sets
    training_data = sentences[:650]
    testing_data = sentences[650:]

    # if testing, run through the testing data sequentially
    if testing:
        for line in testing_data:
            # run the neural net with 0 for epoch because it is not needed
            run(line, model, neural_nets, 0, testing)
        # print accuracy results when done
        pct = (correct_guesses / total_guesses) * 100.0
        print('%.04f%% correct\n' % pct)
        exit(0)

    # if training, pick random sentences
    else:
        for epoch in range(epochs):
            line = random.choice(training_data)
            run(line, model, neural_nets, epoch, testing)
            # if an output file is specified, save the network every 10000 epochs
            if epoch % 10000 == 0:
                if args.output is not None:
                    with open(args.output, 'wb') as output_file:
                        pickle.dump(neural_nets, output_file, -1)

    # save the network after training, if output is specified
    if args.output is not None and not testing:
        with open(args.output, 'wb') as output_file:
            pickle.dump(neural_nets, output_file, -1)
        exit(0)


# run function, handles getting parts of speech for each word,
# making predictions, and adjusting weights
def run(line, model, neural_nets, epoch, testing):
    global total_guesses
    global correct_guesses
    # if word type is unknown, there is no correct answer
    correct_ans = -1

    # break sentence into a list of tokens, removing punctuation
    tokens = gensim.utils.simple_preprocess(line)
    # make a list of tuples in form (word, part_of_speech)
    tagged_line = nltk.pos_tag(tokens)
    # extract parts of speech from tuples
    tags = [pos for __, pos in tagged_line]

    # replace the detailed tags from nltk with simple ones
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

    # get the Word2Vec vector for each word
    vectors = [model[word] for word in tokens]

    # make a prediction for each word
    for i in range(len(tokens)):
        guess = neural_nets[i].predict(vectors[i])
        # convert the number returned into a string guess
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
        # unknown should never occur as output, because the output is an array 0 to 4
        else:
            guess_pos = 'unknown'

        # if we are training, we also need a numeric form of the correct answer to pass into adjust_weights
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

        # word tagged with unknown are ones that we are not trying to identify, so ignore those results
        if tags[i] != 'unknown':
            # increment guesses, total always, correct if we got it right
            total_guesses += 1
            if guess_pos == tags[i]:
                correct_guesses += 1
            # adjust the weights if training
            if not testing:
                neural_nets[i].adjust_weights(vectors[i], correct_ans)

    # during training, print an accuracy update every 100 epochs
    if epoch % 100 == 0 and not testing:
        print('epoch', epoch)
        pct = (correct_guesses / total_guesses) * 100.0
        print('%.04f%% correct\n' % pct)


if __name__ == '__main__':
    main()
