import nltk
import gensim
import neural_net as nn
import random
import pickle

nltk.download('averaged_perceptron_tagger')

print('Loading Word2Vec model, please wait...')
model = gensim.models.KeyedVectors.load_word2vec_format('trained-model.bin', binary=True)
print('Word2Vec model loaded.')

eta = .01
neural_nets = None

if input('open existing neural network? (y/n) ').lower() == 'y':
    with open('neural_networks.pkl', 'rb') as input_file:
        neural_nets = pickle.load(input_file)
if neural_nets is None:
    neural_nets = [nn.NeuralNetwork(eta) for __ in range(10)]
with open('sentences') as file:
    sentences = [line.rstrip('\n.,').replace(' to ', ' ').replace(' and ', ' ')
                     .replace(' of ', ' ').replace('To ', '') for line in file]

training_data = sentences[:649]
testing_data = sentences[650:]

total_guesses = 0
correct_guesses = 0

for epoch in range(100000):
    line = random.choice(training_data)
    # line = training_data[142]
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
    # print(tokens)
    # print(tags)
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
        else:
            correct_ans = -1

        total_guesses += 1
        if guess_pos == tags[i]:
            correct_guesses += 1

        neural_nets[i].adjust_weights(vectors[i], correct_ans)

    if epoch % 10 == 0:
        print('epoch', epoch)
        pct = (correct_guesses / total_guesses) * 100.0
        print('%.04f%% correct\n' % pct)

if input('save neural network? (y/n) ').lower() == 'y':
    with open('neural_networks.pkl', 'wb') as output_file:
        pickle.dump(neural_nets, output_file, -1)

# for line in testing_data:

#
#
# for i in range(len(tokens)):
#     print('\n', tokens[i])
#     print (vectors[i])
#
# exit(0)
