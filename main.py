import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import gensim
from gensim.models import Word2Vec
import random
import neural_net as nn

print('Loading Word2Vec model, please wait...')
model = gensim.models.KeyedVectors.load_word2vec_format('trained-model.bin', binary=True)
print('Word2Vec model loaded.')


tokens = nltk.word_tokenize('')
vectors = [model[w] for w in tokens]

for i in range(len(tokens)):
    print('\n', tokens[i])
    print (vectors[i])