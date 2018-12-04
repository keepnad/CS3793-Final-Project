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
    words[-1] = words[-1][:-1]

    morphFlag = 0
    i = 0
    while i < len(words):
        # print (words[i])
        # print (wordD)
        if words[i] in articles:
            tmp = (words[i], "article")
            wordD.append(tmp)
        elif words[i] in preps:
            tmp = (words[i], "preposition")
            wordD.append(tmp)

        elif i + 1 < len(words) and words[i] in adj and words[i + 1] in nouns:
            tmp = (words[i], "adjective")
            wordD.append(tmp)
            tmp = (words[i + 1], "noun")
            wordD.append(tmp)
            i += 1

        elif i + 1 < len(words) and words[i] in adv and words[i + 1] in adj and words[i + 1] not in preps:
            tmp = (words[i], "adverb")
            wordD.append(tmp)
            tmp = (words[i + 1], "verb")
            wordD.append(tmp)
            i += 1

        elif words[i] in verbs:
            tmp = (words[i], "verb")
            wordD.append(tmp)
        elif words[i] in adj:
            tmp = words[i], "adjective"
            wordD.append(tmp)
        elif words[i] in nouns:
            tmp = (words[i], "noun")
            wordD.append(tmp)
        # elif "'" in words[i]:
        #   tmp = (words[i],"conjunction")
        #   wordD.append(tmp)
        else:
            if morphFlag == 0:
                words[i] = wn.morphy(words[i])
                i -= 1
                morphFlag = 1
            else:
                tmp = (words[i], "unkown")
                wordD.append(tmp)

        i += 1

    print(wordD, "\n")
