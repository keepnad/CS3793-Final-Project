from nltk.corpus import wordnet as wn
import collections

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
   words[-1] = words[-1][:-1]

   doFlag = 0
   ioFlag = 0
   i = 0
   while i < len(words):
   	if words[i] in articles:
	   tmp = (words[i],"article")
	   wordD.append(tmp)
	elif words[i] in preps:
	   tmp = (words[i],"preposition")
	   wordD.append(tmp)
	elif i+1 < len(words) and words[i] in nouns and words[i+1] in nouns:
		tmp = (words[i],"adjective")
	   	wordD.append(tmp)
	   	if doFlag == 0:
	   	   tmp = (words[i+1],"directObj")
	     	   wordD.append(tmp)
		   doFlag = 1
	   	else:
	  	   tmp = (words[i+1],"indirectObj")
		   wordD.append(tmp)
		   ioFlag = 1
	   	i += 1

	elif words[i] in verbs:
	   tmp = (words[i],"verb")
           wordD.append(tmp)
	elif words[i] in adj:
	   tmp = words[i],"adjective"
	   wordD.append(tmp)
	elif words[i] in nouns:
	   if doFlag == 0:
		tmp = (words[i],"directObj")
	   else:
		tmp = (words[i],"indirectObj")
	   wordD.append(tmp)
	else:
	   words[i] = wn.morphy(words[i])
	   if words[i] in verbs:
		i -= 1
	   else:
		i -= 2
	i+=1

   print wordD

