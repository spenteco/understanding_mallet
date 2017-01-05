#!/usr/bin/python
import sys, codecs

# ----------------------------------------------------------------------
# 
# ----------------------------------------------------------------------

def justify(s, resultSize):
    
    resultS = str(s)
    while len(resultS) < resultSize + 1:
        resultS = " " + resultS
    return resultS

def pad(s, resultSize):
    
    resultS = s
    while len(resultS) < resultSize + 1:
        resultS = resultS + " "
    return resultS

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

if len(sys.argv) != 2:
    print "USAGE: stateReport.py inputFile"
    print len(sys.argv)
    sys.exit(2)

#
#   SAVE FOR LATER
#

#documentFrequencyReport = sys.argv[2]

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

letterTopics = {}
topicsLetters = {}

for l in stateFileLines:
    
    if l.startswith("#") == False:
        
        f = l.split(" ")
        
        if len(f) > 1:
            
            word = f[4]
            letter = word[0:1]
            topic = int(f[5])

            try:
                noop = letterTopics[letter]
            except KeyError:
                letterTopics[letter] = {}
                
            try:
                letterTopics[letter][topic] = letterTopics[letter][topic] + 1
            except KeyError:
                letterTopics[letter][topic] = 1

            try:
                noop = topicsLetters[topic]
            except KeyError:
                topicsLetters[topic] = {}
                
            try:
                topicsLetters[topic][letter] = topicsLetters[topic][letter] + 1
            except KeyError:
                topicsLetters[topic][letter] = 1

#
#   TURN THE HASHES INTO MATRICES
#
                
letters = sorted(letterTopics.keys())
topics  = sorted(topicsLetters.keys())

letterTopicMatrix = []

for letter in letters:
    matrixRow = []
    for topic in topics:
        wordCount = 0
        try:
            wordCount = letterTopics[letter][topic]
        except KeyError:
            noop = 0
        matrixRow.append(wordCount)
    letterTopicMatrix.append(matrixRow)

topicLetterMatrix = []

for topic in topics:
    matrixRow = []
    for letter in letters:
        wordCount = 0
        try:
            wordCount = topicsLetters[topic][letter]
        except KeyError:
            noop = 0
        matrixRow.append(wordCount)
    topicLetterMatrix.append(matrixRow)

#
#   DUMP THE MATRICES TO STDOUT
#

print
outLine = "letters-topics " + "topic "
for a in range(0, len(topics)):
    outLine = outLine + " " + justify(str(topics[a]), 5)
print outLine

for a in range(0, len(letters)):
    outLine = "letters-topics " + pad(str(letters[a]), 5)
    for b in range(0, len(topics)):
        outLine = outLine + " " + justify(str(letterTopicMatrix[a][b]), 5)
    print outLine

print
outLine = "topics-letters " + "topic "
for a in range(0, len(letters)):
    outLine = outLine + " " + justify(str(letters[a]), 5)
print outLine

for a in range(0, len(topics)):
    outLine = "topics-letters " + pad(str(topics[a]), 5)
    for b in range(0, len(letters)):
        outLine = outLine + " " + justify(str(topicLetterMatrix[a][b]), 5)
    print outLine

# ----------------------------------------------------------------------
#   MEASURE TOPIC-DOCUMENT SEGREGATION
# ----------------------------------------------------------------------

print
for a in range(0, len(letters)):
    
    numberOfWords = 0
    highTopicNumberOfWords = 0
    highTopic = -1
    
    for b in range(0, len(topics)):
        
        numberOfWords = numberOfWords + letterTopicMatrix[a][b]
        if letterTopicMatrix[a][b] > highTopicNumberOfWords:
            highTopicNumberOfWords = letterTopicMatrix[a][b]
            highTopic = topics[b]
            
    segregationRatio = float(highTopicNumberOfWords) / float(numberOfWords)
            
    print "topic/document seg " + pad(str(letters[a]), 3) + " numberOfWords " + justify(numberOfWords, 5) + " highTopic " + justify(highTopic, 2) + " highTopicNumberOfWords " + justify(highTopicNumberOfWords, 5) + " segregation " + str(segregationRatio)[0:4]

#
#   FIND WORDS THAT WEREN'T TOPIC-DOCUMENT SEGREGATED
#

problemWords = {}
okayWords = {}

print
for a in range(0, len(letters)):
    
    numberOfWords = 0
    highTopicNumberOfWords = 0
    highTopic = -1
    
    for b in range(0, len(topics)):
        
        numberOfWords = numberOfWords + letterTopicMatrix[a][b]
        if letterTopicMatrix[a][b] > highTopicNumberOfWords:
            highTopicNumberOfWords = letterTopicMatrix[a][b]
            highTopic = topics[b]

    for l in stateFileLines:
        
        if l.startswith("#") == False:
            
            f = l.split(" ")
            
            if len(f) > 1:
                
                word = f[4]
                letter = word[0:1]
                topic = int(f[5])
                
                if letter == letters[a]:
                    if  topic == highTopic:
                        okayWords[word] = 1
                    else:
                        problemWords[word] = 1
                        
print "topic-document okayWords (unique)", len(sorted(okayWords.keys())), float(len(okayWords.keys())) / float(len(okayWords.keys()) + len(problemWords.keys()))                  
print "topic-document problemWords (unique)", len(sorted(problemWords.keys())), float(len(problemWords.keys())) / float(len(okayWords.keys()) + len(problemWords.keys()))

#inF = codecs.open(documentFrequencyReport, "r", "utf-8")
#documentFrequency = inF.read().split("\n")
#inF.close()

#
#   FIND TOPIC-DOCUMENT UN-SEGREGATED WORDS IN DOCUMENT FREQUENCY DATA
#

#allDocumentFrequencies = {}
#problemDocumentFrequencies = {}
    
#for line in documentFrequency:
#    if line.strip() > "" and line.startswith("Document Freqencies") == False:
#        word = line.split(" ")[0]
#        docFreq = int(line.split(" ")[1])
#        try:
#            allDocumentFrequencies[docFreq] = allDocumentFrequencies[docFreq] + 1
#        except KeyError:
#            allDocumentFrequencies[docFreq] = 1
            
#for word in sorted(problemWords.keys()):
#    for line in documentFrequency:
#       if line.startswith(word):
#            word = line.split(" ")[0]
#            docFreq = int(line.split(" ")[1])
#            try:
#                problemDocumentFrequencies[docFreq] = problemDocumentFrequencies[docFreq] + 1
#            except KeyError:
#                problemDocumentFrequencies[docFreq] = 1
                
#print
#print "topic-document frequency accuracy rate"
#print
#print justify("freq", 4) + " " + justify("words", 5) + " " + justify("error", 5) + " " + justify("rate", 5)
#for k in sorted(allDocumentFrequencies.keys()):
#    errorDF = 0
#    try:
#        errorDF = problemDocumentFrequencies[k]
#    except KeyError:
#        noop = 0
#    accuracyRate = float(allDocumentFrequencies[k] - errorDF) / float(allDocumentFrequencies[k])
#    print justify(k, 4) + " " + justify(allDocumentFrequencies[k], 5) + " " + justify(errorDF, 5) + " " + justify((str(accuracyRate) + "0")[0:4], 5)


# ----------------------------------------------------------------------
#   MEASURE DOCUMENT-TOPIC SEGREGATION
# ----------------------------------------------------------------------

print
for a in range(0, len(topics)):
    
    numberOfWords = 0
    highLetterNumberOfWords = 0
    highLetter = -1
    
    for b in range(0, len(letters)):
        
        numberOfWords = numberOfWords + topicLetterMatrix[a][b]
        if topicLetterMatrix[a][b] > highLetterNumberOfWords:
            highLetterNumberOfWords = topicLetterMatrix[a][b]
            highLetter = letters[b]
            
    segregationRatio = float(highLetterNumberOfWords) / float(numberOfWords)
            
    print "document/topic seg " + pad(str(topics[a]), 3) + " numberOfWords " + justify(numberOfWords, 5) + " highLetter " + justify(highLetter, 2) + " highLetterNumberOfWords " + justify(highLetterNumberOfWords, 5) + " segregation " + str(segregationRatio)[0:4]

#
#   FIND WORDS THAT WEREN'T DOCUMENT-TOPIC SEGREGATED
#

problemWords = {}
okayWords = {}

print
for a in range(0, len(topics)):
    
    numberOfWords = 0
    highLetterNumberOfWords = 0
    highLetter = -1
    
    for b in range(0, len(letters)):
        
        numberOfWords = numberOfWords + topicLetterMatrix[a][b]
        if topicLetterMatrix[a][b] > highLetterNumberOfWords:
            highLetterNumberOfWords = topicLetterMatrix[a][b]
            highLetter = letters[b]

    for l in stateFileLines:
        
        if l.startswith("#") == False:
            
            f = l.split(" ")
            
            if len(f) > 1:
                
                word = f[4]
                letter = word[0:1]
                topic = int(f[5])
                
                if  topic == topics[a]:
                    if  letter == highLetter:
                        okayWords[word] = 1
                    else:
                        problemWords[word] = 1
                        
print "document-topic okayWords (unique)", len(sorted(okayWords.keys())), float(len(okayWords.keys())) / float(len(okayWords.keys()) + len(problemWords.keys()))                  
print "document-topic problemWords (unique)", len(sorted(problemWords.keys())), float(len(problemWords.keys())) / float(len(okayWords.keys()) + len(problemWords.keys()))

#inF = codecs.open(documentFrequencyReport, "r", "utf-8")
#documentFrequency = inF.read().split("\n")
#inF.close()

#
#   FIND DOCUMENT-TOPIC UN-SEGREGATED WORDS IN DOCUMENT FREQUENCY DATA
#

#allDocumentFrequencies = {}
#problemDocumentFrequencies = {}
    
#for line in documentFrequency:
#    if line.strip() > "" and line.startswith("Document Freqencies") == False:
#        word = line.split(" ")[0]
#        docFreq = int(line.split(" ")[1])
#        try:
#            allDocumentFrequencies[docFreq] = allDocumentFrequencies[docFreq] + 1
#        except KeyError:
#            allDocumentFrequencies[docFreq] = 1
            
#for word in sorted(problemWords.keys()):
#    for line in documentFrequency:
#        if line.startswith(word):
#            word = line.split(" ")[0]
#            docFreq = int(line.split(" ")[1])
#            try:
#                problemDocumentFrequencies[docFreq] = problemDocumentFrequencies[docFreq] + 1
#            except KeyError:
#                problemDocumentFrequencies[docFreq] = 1
                
#print
#print "topic-document frequency accuracy rate"
#print
#print justify("freq", 4) + " " + justify("words", 5) + " " + justify("error", 5) + " " + justify("rate", 5)
#for k in sorted(allDocumentFrequencies.keys()):
#    errorDF = 0
#    try:
#        errorDF = problemDocumentFrequencies[k]
#    except KeyError:
#        noop = 0
#    accuracyRate = float(allDocumentFrequencies[k] - errorDF) / float(allDocumentFrequencies[k])
#    print justify(k, 4) + " " + justify(allDocumentFrequencies[k], 5) + " " + justify(errorDF, 5) + " " + justify((str(accuracyRate) + "0")[0:4], 5)
