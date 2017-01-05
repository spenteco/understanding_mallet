#!/usr/bin/python

import sys, codecs, re, os, commands, time, string, random, logging

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def justifyAndZeroFill(s):
    result = s
    while len(result) < 4:
        result = "0" + result
    return result

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def generateSimpleTexts(textsFolder, topicsFolder, numberOfTexts, sizeOfTexts, lowNbrTopics, highNbrTopics):
    
    logging.info("generateSimpleTexts numberOfTexts " + str(numberOfTexts) + " sizeOfTexts " + str(sizeOfTexts) + " lowNbrTopics " + str(lowNbrTopics)  + " highNbrTopics " + str(highNbrTopics)  + "\n")
    
    topics = {}
    
    for fileName in os.listdir(topicsFolder):

        if fileName.endswith(".txt"):
            
            inF = codecs.open(topicsFolder + fileName, "r", encoding="utf-8")
            topicWords = inF.read().strip().split("\n")
            inF.close()
            
            topics[fileName.replace(".txt", "")] = topicWords
            
    topicKeys = sorted(topics.keys())
    
    for a in range(0, numberOfTexts):
    
        numberOfTopics = random.randint(lowNbrTopics, highNbrTopics)
           
        topicDistribution = {}
        
        numberOfTopicsFound = 0
        while numberOfTopicsFound < numberOfTopics:
            
            nextTopic = topicKeys[random.randint(0, len(topicKeys) - 1)]
            
            try:
                noop = topicDistribution[nextTopic]
            except KeyError:
                topicDistribution[nextTopic] = {"topicRatio": 0.0, "numberOfWords": 0}
                numberOfTopicsFound = numberOfTopicsFound + 1
                
        for topic in sorted(topicDistribution.keys()):
            topicDistribution[topic]["topicRatio"] = 1.0 / numberOfTopics
            topicDistribution[topic]["numberOfWords"] = sizeOfTexts / numberOfTopics
            
        logging.info("")    
        logging.info("generateSimpleTexts outputText " + justifyAndZeroFill(str(a)) + ".txt" + " numberOfTopics " + str(numberOfTopics))
        for topic in sorted(topicDistribution.keys()):
            logging.info("generateSimpleTexts topic " + topic + " topicRatio "  + str(topicDistribution[topic]["topicRatio"]) + " numberOfWords " + str(topicDistribution[topic]["numberOfWords"]))
            
        wordsInText = []
        for topic in sorted(topicDistribution.keys()):
            for n in range(0, topicDistribution[topic]["numberOfWords"]):
                wordsInText.append(topics[topic][random.randint(0, len(topics[topic]) - 1)])
                
        random.shuffle(wordsInText)
                
        outF = codecs.open(textsFolder + justifyAndZeroFill(str(a)) + ".txt", "w", encoding="utf-8")
        for w in wordsInText:
            outF.write(w + "\n")
        outF.close()

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def generateZipfTexts(textsFolder, topicsFolder, numberOfTexts, sizeOfTexts, lowNbrTopics, highNbrTopics):
    
    logging.info("generateZipfTexts numberOfTexts " + str(numberOfTexts) + " sizeOfTexts " + str(sizeOfTexts) + " lowNbrTopics " + str(lowNbrTopics)  + " highNbrTopics " + str(highNbrTopics)  + "\n")
    
    topics = {}
    
    for fileName in os.listdir(topicsFolder):

        if fileName.endswith(".txt"):
            
            inF = codecs.open(topicsFolder + fileName, "r", encoding="utf-8")
            lines = inF.read().strip().split("\n")
            inF.close()
            
            topicWords = []
            
            for l in lines:
                if l.strip() > "":
                    topicWords.append({"word": l.strip(), "maximumAllowedDf": 9999, "actualDf": 0})
            
            for i in range(1, int(len(topicWords) * 0.40)):
                topicWords[i]["maximumAllowedDf"] = 1
            
            for i in range(int(len(topicWords) * 0.40), int(len(topicWords) * 0.50)):
                topicWords[i]["maximumAllowedDf"] = 2
            
            for i in range(int(len(topicWords) * 0.55), int(len(topicWords) * 0.60)):
                topicWords[i]["maximumAllowedDf"] = 3
            
            topics[fileName.replace(".txt", "")] = topicWords
            
    topicKeys = sorted(topics.keys())
    
    for a in range(0, numberOfTexts):
    
        numberOfTopics = random.randint(lowNbrTopics, highNbrTopics)
           
        topicDistribution = {}
        
        numberOfTopicsFound = 0
        while numberOfTopicsFound < numberOfTopics:
            
            nextTopic = topicKeys[random.randint(0, len(topicKeys) - 1)]
            
            try:
                noop = topicDistribution[nextTopic]
            except KeyError:
                topicDistribution[nextTopic] = {"topicRatio": 0.0, "numberOfWords": 0}
                numberOfTopicsFound = numberOfTopicsFound + 1
                
        for topic in sorted(topicDistribution.keys()):
            topicDistribution[topic]["topicRatio"] = 1.0 / numberOfTopics
            topicDistribution[topic]["numberOfWords"] = sizeOfTexts / numberOfTopics
            
        logging.info("")    
        logging.info("generateSimpleTexts outputText " + justifyAndZeroFill(str(a)) + ".txt" + " numberOfTopics " + str(numberOfTopics))
        for topic in sorted(topicDistribution.keys()):
            logging.info("generateSimpleTexts topic " + topic + " topicRatio "  + str(topicDistribution[topic]["topicRatio"]) + " numberOfWords " + str(topicDistribution[topic]["numberOfWords"]))
            
        wordsInText = []
        for topic in sorted(topicDistribution.keys()):
            
            wordsWritten = 0
            
            while wordsWritten < topicDistribution[topic]["numberOfWords"]:
                
                nextWord = topics[topic][random.randint(0, len(topics[topic]) - 1)]
                
                if nextWord["actualDf"] < nextWord["maximumAllowedDf"]:
                    
                    wordsInText.append(nextWord["word"])
                    
                    nextWord["actualDf"] = nextWord["actualDf"] + 1 
                    wordsWritten = wordsWritten + 1
                    
        outF = codecs.open(textsFolder + justifyAndZeroFill(str(a)) + ".txt", "w", encoding="utf-8")
        for w in wordsInText:
            outF.write(w + "\n")
        outF.close()


# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def generateZipfTextsWithZ(textsFolder, topicsFolder, numberOfTexts, sizeOfTexts, lowNbrTopics, highNbrTopics, nbrZwords):
    
    logging.info("generateZipfTexts numberOfTexts " + str(numberOfTexts) + " sizeOfTexts " + str(sizeOfTexts) + " lowNbrTopics " + str(lowNbrTopics)  + " highNbrTopics " + str(highNbrTopics)  + "\n")
    
    topics = {}
    zTopic = []
    
    for fileName in os.listdir(topicsFolder):

        if fileName.endswith(".txt") and fileName.startswith("Z") == False:
            
            inF = codecs.open(topicsFolder + fileName, "r", encoding="utf-8")
            lines = inF.read().strip().split("\n")
            inF.close()
            
            topicWords = []
            
            for l in lines:
                if l.strip() > "":
                    topicWords.append({"word": l.strip(), "maximumAllowedDf": 9999, "actualDf": 0})
            
            for i in range(1, int(len(topicWords) * 0.40)):
                topicWords[i]["maximumAllowedDf"] = 1
            
            for i in range(int(len(topicWords) * 0.40), int(len(topicWords) * 0.50)):
                topicWords[i]["maximumAllowedDf"] = 2
            
            for i in range(int(len(topicWords) * 0.55), int(len(topicWords) * 0.60)):
                topicWords[i]["maximumAllowedDf"] = 3
            
            topics[fileName.replace(".txt", "")] = topicWords
            
    inF = codecs.open(topicsFolder + "Z.txt", "r", encoding="utf-8")
    lines = inF.read().strip().split("\n")
    inF.close()
            
    topicKeys = sorted(topics.keys())
            
    for l in lines:
        if l.strip() > "":
            zTopic.append(l.strip())
    
    for a in range(0, numberOfTexts):
    
        numberOfTopics = random.randint(lowNbrTopics, highNbrTopics)
           
        topicDistribution = {}
        
        numberOfTopicsFound = 0
        while numberOfTopicsFound < numberOfTopics:
            
            nextTopic = topicKeys[random.randint(0, len(topicKeys) - 1)]
            
            try:
                noop = topicDistribution[nextTopic]
            except KeyError:
                topicDistribution[nextTopic] = {"topicRatio": 0.0, "numberOfWords": 0}
                numberOfTopicsFound = numberOfTopicsFound + 1
                
        for topic in sorted(topicDistribution.keys()):
            topicDistribution[topic]["topicRatio"] = 1.0 / numberOfTopics
            topicDistribution[topic]["numberOfWords"] = sizeOfTexts / numberOfTopics
            
        logging.info("")    
        logging.info("generateSimpleTexts outputText " + justifyAndZeroFill(str(a)) + ".txt" + " numberOfTopics " + str(numberOfTopics))
        for topic in sorted(topicDistribution.keys()):
            logging.info("generateSimpleTexts topic " + topic + " topicRatio "  + str(topicDistribution[topic]["topicRatio"]) + " numberOfWords " + str(topicDistribution[topic]["numberOfWords"]))
            
        wordsInText = []
        for topic in sorted(topicDistribution.keys()):
            
            wordsWritten = 0
            
            while wordsWritten < topicDistribution[topic]["numberOfWords"]:
                
                nextWord = topics[topic][random.randint(0, len(topics[topic]) - 1)]
                
                if nextWord["actualDf"] < nextWord["maximumAllowedDf"]:
                    
                    wordsInText.append(nextWord["word"])
                    
                    nextWord["actualDf"] = nextWord["actualDf"] + 1 
                    wordsWritten = wordsWritten + 1
          
        random.shuffle(zTopic)
        for b in range(0, nbrZwords):
            wordsInText.append(zTopic[b])
                
        random.shuffle(wordsInText)
                
        outF = codecs.open(textsFolder + justifyAndZeroFill(str(a)) + ".txt", "w", encoding="utf-8")
        for w in wordsInText:
            outF.write(w + "\n")
            
        outF.close()
