#!/usr/bin/python

import sys, codecs

# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

if len(sys.argv) != 2:
    print "USAGE: reorderTopicsInDocFile.py inputFile"
    print len(sys.argv)
    sys.exit(2)

inputFile = sys.argv[1]
outputFile = inputFile.replace(".doc.txt", ".matrix.doc.csv")

inF = codecs.open(inputFile, "r", "utf-8") 
outF = codecs.open(outputFile, "w", "utf-8") 

lines = inF.read().split("\n")

topicNumbers = []

for l in lines:

    if l[0:1] != "#":
        fields = l.strip().replace("./Text_Files/", "").split(" ")

        if len(fields) > 1:

            fileNumber = fields[0]
            fileName = fields[1]
            topicData = {}

            f = 2
            while f < len(fields) - 1:

                topicData[int(fields[f])] = fields[f + 1] 

                f = f + 2
                
            topicNumbers = sorted(topicData.keys())
            
            break;

sortedLines = {}

for l in lines:

    if l[0:1] != "#":
        fields = l.strip().replace("./Text_Files/", "").split(" ")

        if len(fields) > 1:

            fileNumber = fields[0]
            fileName = fields[1]
            topicData = {}

            f = 2
            while f < len(fields) - 1:

                topicData[int(fields[f])] = fields[f + 1] 

                f = f + 2

            outLine = fileName
            for n in topicNumbers:
                outLine = outLine + "," + str(float(topicData[n]))
            outLine = outLine + "\n"
            
            sortedLines[fileName] = outLine
       
outLine = "label"
for n in topicNumbers:
    outLine = outLine + "," + str(n)
outF.write(outLine + "\n")
            
for k in sorted(sortedLines.keys()):
    outF.write(sortedLines[k])

inF.close()
outF.close()
