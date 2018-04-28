import sys
import pandas as pd 
import time
import re
from datetime import datetime, timedelta
import string
import zlib

data = pd.read_csv('analyzed.csv')
counts = dict()
for text in data['Tweets']:
    map = str.maketrans('', '', string.punctuation)
    text = text.translate(map)
    map = str.maketrans('', '', '1234567890')
    text = text.translate(map)
    text = text.strip()
    text = text.lower()
    words = text.split()
    #print text
    for word in words:
        if len(word) < 4 : continue
        counts[word] = counts.get(word,0) + 1
        
# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for w in words[:100]:
    if highest is None or highest < counts[w] :
        highest = counts[w]
    if lowest is None or lowest > counts[w] :
        lowest = counts[w]
print ('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 100
smallsize = 20

fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in words[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print ("Output written to gword.js")
print ("Open gword.htm in a browser to view")