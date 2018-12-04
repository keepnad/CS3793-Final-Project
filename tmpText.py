from nltk.corpus import wordnet as wn
from func import tagWord

articles = ['a','an','the']

with open("adj","r") as file1:
   adj = file1.read().splitlines()

with open("nouns","r") as file2:
   nouns = file2.read().splitlines()

with open("verbs","r") as file3:
   verbs = file3.read().splitlines()

with open('preps') as f:
    preps = f.read().splitlines()

for line in open("sentences",'r'):
   wordD = []
   words = line.split()
   print words
   words[0] = words[0][0].lower() + words[0][1:] #lower case first word

   doFlag = 0
   ioFlag = 0
   i = 0
   while i < len(words):
        tmp = tagWord(words,articles,adj,nouns,verbs,preps,i)
        wordD.append(tmp)
        i+=1

   print wordD

