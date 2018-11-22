from PyDictionary import PyDictionary

dictionary = PyDictionary();

definition = dictionary.meaning("animal");

for part_of_speech in definition:
    print(part_of_speech);