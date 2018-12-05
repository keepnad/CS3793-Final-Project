# Daniel Peek qer419
# Michael Canas ohh135
# CS 3793 Final Project
# 12/4/18

import nltk
from nltk.corpus import wordnet as wn
# install the needed wordnet module, if not present
nltk.download('wordnet')

# Dictionaryies difined for articles,adverbs,adjectives,nouns,verbs,preps
articles = ['a', 'an', 'the', 'these', 'this']

with open("adverbs", "r") as file0:
    adv = file0.read().splitlines()

with open("adj", "r") as file1:
    adj = file1.read().splitlines()

with open("nouns", "r") as file2:
    nouns = file2.read().splitlines()

with open("verbs", "r") as file3:
    verbs = file3.read().splitlines()

with open('preps') as f:
    preps = f.read().splitlines()

#Parse through each line in the file
for line in open("sentences", 'r'):
    wordD = []
    words = line.split() #split line into word tokens
    print(words)
    words[0] = words[0][0].lower() + words[0][1:]  # lower case first word
    words[-1] = words[-1][:-1]  # remove periods

    # check if any words not in any dictionary
    j = 0
    for w in words:
        if w not in articles and w not in adj and w not in adv and w not in nouns and w not in verbs and w not in preps:
            #if word is not in dictionary use morphy to change word to its base word
            words[j] = wn.morphy(w)
        j += 1

    i = 0
    #parse while i is less then length of sentence
    while i < len(words):
        # check four worded patterns
        if i + 3 < len(words):
            # Check for patter: article noun verb verb
            if words[i] in articles and words[i + 1] in nouns and words[i + 2] in verbs and words[i + 3] in verbs:
                # Save word and part of speach into a tuple and append to dictionary
                tmp = (words[i], "article")
                wordD.append(tmp)
                tmp = (words[i + 1], "noun")
                wordD.append(tmp)
                tmp = (words[i + 2], "verb")
                wordD.append(tmp)
                tmp = (words[i + 3], "verb")
                wordD.append(tmp)
                i += 4
                continue

        # check 3 worded pattens
        if i + 2 < len(words):
            # check for pattern:"article" "adj" "noun"
            if words[i] in articles and words[i + 1] in adj and words[i + 2] in nouns:
                # Save word and part of speach into a tuple and append to dictionary                
                tmp = (words[i], "article")
                wordD.append(tmp)
                tmp = (words[i + 1], "adjective")
                wordD.append(tmp)
                tmp = (words[i + 2], "noun")
                wordD.append(tmp)
                i += 3
                continue
                # check for pattern:"art" "noun" "verb"
            elif words[i] in articles and words[i + 1] in nouns and words[i + 2] in verbs:
                # Save word and part of speach into a tuple and append to dictionary
                tmp = (words[i], "article")
                wordD.append(tmp)
                tmp = (words[i + 1], "noun")
                wordD.append(tmp)
                tmp = (words[i + 2], "verb")
                wordD.append(tmp)
                i += 3
                continue
        # check 2 worded paterns
        if i + 1 < len(words):
            #Check for pattern: adverb verb
            if words[i] in adv and words[i + 1] in verbs:
                tmp = (words[i], "adverb")
                wordD.append(tmp)
                tmp = (words[i + 1], "verb")
                wordD.append(tmp)
                i += 2
                continue
            #Check for pattern: article noun
            if words[i] in articles and words[i + 1] in nouns:
                tmp = (words[i], "article")
                wordD.append(tmp)
                tmp = (words[i + 1], "noun")
                wordD.append(tmp)
                i += 2
                continue
        # if patterns not matched tag with dictonary lookup
        if words[i] in preps:
            tmp = (words[i], "preposition")
            wordD.append(tmp)
            i += 1
            continue
        if words[i] in verbs:
            tmp = (words[i], "verb")
            wordD.append(tmp)
            i += 1
            continue
        if words[i] in adv:
            tmp = (words[i], "adverb")
            wordD.append(tmp)
            i += 1
            continue
        if words[i] in articles:
            tmp = (words[i], "article")
            wordD.append(tmp)
            i += 1
            continue
        i += 1

    print(wordD)
    print()
