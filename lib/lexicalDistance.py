#!/usr/bin/python
import sys, codecs

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

if len(sys.argv) != 2:
    print "USAGE: lexicalDistance.py inputFile"
    print len(sys.argv)
    sys.exit(2)

#
#   LOAD THE STATE FILE
#

inputFile = sys.argv[1]


inF = codecs.open(inputFile, "r", "utf-8")
stateFileLines = inF.read().split("\n")
inF.close()

#
#   HASH UP THE STATE FILE
#

topicWords = {}

for l in stateFileLines:
    
    if l.startswith("#") == False:
        
        f = l.split(" ")
        
        if len(f) > 1:
            
            word = f[4]
            letter = word[0:1]
            topic = int(f[5])

            try:
                noop = topicWords[topic]
            except KeyError:
                topicWords[topic] = []
                
            topicWords[topic].append(word)

for topic, words in topicWords.iteritems():
    words = set(words)


#
#   MEASURE THE LEXICAL COHERENCE FOR EACH TOPIC
#



numberComparedRun = 0
totalLexicalDistanceRun = 0

for topic, words in topicWords.iteritems():
    
    numberCompared = 0
    totalLexicalDistance = 0
    
    for a in range(0, len(words) - 1):
        for b in range(a + 1, len(words)):
            
            numberCompared += 1
            numberComparedRun += 1
            
            if words[a][0] != words[b][0]:
                totalLexicalDistance += 1
                totalLexicalDistanceRun += 1
                
    print topic, numberCompared, totalLexicalDistance, (float(totalLexicalDistance) / float(numberCompared))
    
print "TOTAL", numberComparedRun, totalLexicalDistanceRun, (float(totalLexicalDistanceRun) / float(numberComparedRun))
    
    
            

