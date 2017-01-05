#!/usr/bin/python
import sys, codecs

# -------------------------------------------------------------------------------------- #
#
# -------------------------------------------------------------------------------------- #

if len(sys.argv) != 3:
    print "USAGE: reorderTopicsInDocFile.py inputFile outputFile"
    print len(sys.argv)
    sys.exit(2)

inputFile = sys.argv[1]
outputFile = sys.argv[2]

inF = codecs.open(inputFile, "r", "utf-8")
outF = codecs.open(outputFile, "w", "utf-8")
lines = inF.read().split("\n")
k = 0
n = 1
docTxt = []
outF.write(" , ,")
numCols = 0
for l in lines:
    if len(l) == 0:
        continue
    fields = l.split(",")
    zipped = [(fields[2*x],fields[2*x+1]) for x in range(len(fields)/2)]
    start = zipped[0]
    zipped = sorted(zipped[1:len(zipped)], key=lambda x: float(x[1]), reverse=True)
    zipped.insert(0,start)
    entryString = ""
    for entry in zipped:
        t, n = entry
        entryString += str(t)
        entryString += ","
        try:
             nTwo=str(n).split("/")
             n=nTwo[len(nTwo - 1)]
        except:
             n=n
        try:
            percentString = "%.2f%%" % (float(n)*100)
            entryString += percentString
        except:
            entryString += str(n)
        entryString += ","
	numCols = len(zipped)
    entryString = entryString[0:len(entryString)-1]
    arrLines = zipped[1][0], entryString
    docTxt.append(arrLines)
for i in range(numCols-1):
    curStr = "Topic " + str(i) + " ,  Pct " + str(i) + ","
    outF.write(curStr)
outF.write("\n")

docTxt = sorted(docTxt, key=lambda x: int(x[0]))
for line in docTxt:
    outF.write(line[1])
    outF.write("\n")
    #print line[1]
inF.close()
outF.close()
