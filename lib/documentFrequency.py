#!/usr/bin/python

import sys, codecs, re, os, commands, time, string, random, logging

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def fixTrailingSlash(s):
    fixedS = s
    if s.endswith("/") == False:
        fixedS = fixedS + "/"
    return fixedS

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

if len(sys.argv) != 2:
    print "USAGE: documentFrequency.py inputFolder"
    print len(sys.argv)
    sys.exit(2)

inputFolder = fixTrailingSlash(sys.argv[1])

allTextFrequencies = {}

for fileName in os.listdir(inputFolder):

    textFrequencies = {}

    inF = codecs.open(inputFolder + fileName, "r", "utf-8")
    lines = inF.read().split("\n")
    inF.close()

    for line in lines:
        if line.strip() > "":
            try:
                textFrequencies[line.lower()] = textFrequencies[line.lower()] + 1
            except KeyError:    
                textFrequencies[line.lower()] = 1
            
    allTextFrequencies[fileName] = textFrequencies
    
documentFrequency = {}

for text, textFrequencies in allTextFrequencies.iteritems():
    for word in textFrequencies.keys():
        try:
            documentFrequency[word] = documentFrequency[word] + 1
        except KeyError:
            documentFrequency[word] = 1
            
sortedDocumentFrequency = []
for k, v in documentFrequency.iteritems():
    sortedDocumentFrequency.append([v, k])

sortedDocumentFrequency = sorted(sortedDocumentFrequency, reverse=True)

print "Document Freqencies"
print ""
for s in sortedDocumentFrequency:
    print s[1] + " " + str(s[0])
    

