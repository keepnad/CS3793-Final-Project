# Daniel Peek qer419
# Michael Canas ohh135
# CS 3793 Final Project
# 12/4/18

from nltk.corpus import wordnet as wn

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

for line in open("sentences", 'r'):
    wordD = []
    words = line.split()
    print(words)
    words[0] = words[0][0].lower() + words[0][1:]  # lower case first word
    words[-1] = words[-1][:-1]  # remove periods

    # check if any words not in any dictionary
    j = 0
    for w in words:
        if w not in articles and w not in adj and w not in adv and w not in nouns and w not in verbs and w not in preps:
            # print w
            words[j] = wn.morphy(w)
            # print w
        j += 1

    i = 0
    while i < len(words):
        if i + 3 < len(words):
            # print "in 4 if"
            # print words[i:i+3]
            if words[i] in articles and words[i + 1] in nouns and words[i + 2] in verbs and words[i + 3] in verbs:
                # print "in 4 storage"
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

        if i + 2 < len(words):
            # print words[i],i
            # check for pattern:"article" "adj" "noun"
            if words[i] in articles and words[i + 1] in adj and words[i + 2] in nouns:
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
                tmp = (words[i], "article")
                wordD.append(tmp)
                tmp = (words[i + 1], "noun")
                wordD.append(tmp)
                tmp = (words[i + 2], "verb")
                wordD.append(tmp)
                i += 3
                continue
        if i + 1 < len(words):
            if words[i] in articles and words[i + 1] in nouns:
                tmp = (words[i], "article")
                wordD.append(tmp)
                tmp = (words[i + 1], "noun")
                wordD.append(tmp)
                i += 2
                continue
        if words[i] in preps:
            tmp = (words[i], "preposition")
            wordD.append(tmp)
        i += 1

    print(wordD)
    print()
