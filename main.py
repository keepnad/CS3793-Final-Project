from PyDictionary import PyDictionary
import random
import neural_net as nn

dictionary = PyDictionary();

definition = dictionary.meaning("animal");

for part_of_speech in definition:
    print(part_of_speech);