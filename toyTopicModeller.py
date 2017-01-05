#!/usr/bin/python

import sys, os, codecs, re, random, time

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

def fixTrailingSlash(s):
    fixedS = s
    if s.endswith('/') == False:
        fixedS = fixedS + '/'
    return fixedS

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------
    
def outputStateFile(textsWordTopicAssignments, outputFolder):
  
    outF = codecs.open(outputFolder + 'toyTopicModeller.state.txt', 'w', encoding='utf-8')
                
    outF.write('#STATE FILE FROM TOY TOPIC MODELLER\n')
    
    for text, wordTopicAssignments in textsWordTopicAssignments.iteritems():
        for wordTopicAssignment in wordTopicAssignments:
        
            outF.write("0 " + text + " 0 0 " + wordTopicAssignment["word"] + " " + str(wordTopicAssignment["topic"]) + "\n")

    outF.close()

# ----------------------------------------------------------------------
#   
# ----------------------------------------------------------------------

def initializeTopicCountArray(numberOfTopics):
    
    topicCountArray = []
    for a in range(0, numberOfTopics):
        topicCountArray.append(0)
        
    return topicCountArray

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def loadCorpus(inputFolder):
    
    corpus = []

    for fileName in os.listdir(inputFolder):

        inF = codecs.open(inputFolder + fileName, 'r', 'utf-8')
        inData = inF.read().strip()
        inF.close()
        
        tokens = re.split('!|\(|\)|\;|\:|\'|"|,|\.|\?|\t|\n|\r| ', inData)
        
        corpus.append({'fileName': fileName, 'words': [t.lower() for t in tokens]})
        
    return corpus

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------
    
def makeMatrices(corpus, numberOfTopics):
    
    textsWordTopicAssignments = {}
    
    for text in corpus:
        textsWordTopicAssignments[text['fileName']] = []
        for word in text['words']:
            textsWordTopicAssignments[text['fileName']].append({'word': word, 'topic': random.randint(0, numberOfTopics - 1)})
                   
    #print '\n textsWordTopicAssignments', textsWordTopicAssignments
        
    distinctWordTopicCounts = {}
    
    for a in range(0, len(corpus)):
        for b in range(0, len(corpus[a]['words'])):
            distinctWordTopicCounts[corpus[a]['words'][b]] = initializeTopicCountArray(numberOfTopics)
    
    for text, wordTopicAssignments in textsWordTopicAssignments.iteritems():
        for wordTopicAssignment in wordTopicAssignments:
            distinctWordTopicCounts[wordTopicAssignment['word']][wordTopicAssignment['topic']] = (
                distinctWordTopicCounts[wordTopicAssignment['word']][wordTopicAssignment['topic']]  + 1)
    
    #print '\n distinctWordTopicCounts', distinctWordTopicCounts
            
    corpusTopicCounts = initializeTopicCountArray(numberOfTopics)
    
    for text, wordTopicAssignments in textsWordTopicAssignments.iteritems():
        for wordTopicAssignment in wordTopicAssignments:
            corpusTopicCounts[wordTopicAssignment['topic']] = corpusTopicCounts[wordTopicAssignment['topic']]  + 1
    
    #print '\n corpusTopicCounts', corpusTopicCounts
    
    textTopicCounts ={}
    
    for text, wordTopicAssignments in textsWordTopicAssignments.iteritems():
        textTopicCounts[text] = initializeTopicCountArray(numberOfTopics)
        for wordTopicAssignment in wordTopicAssignments:
            textTopicCounts[text][wordTopicAssignment['topic']] = textTopicCounts[text][wordTopicAssignment['topic']] + 1
            
    #print '\n textTopicCounts', textTopicCounts
        
    return textsWordTopicAssignments, distinctWordTopicCounts, corpusTopicCounts, textTopicCounts
                
# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def scaleDistributionTo1(inputDistribution):    
                        
        #print '\n inputDistribution', inputDistribution
          
        totalDistribution = 0
        
        for a in range(0, len(inputDistribution)):
            totalDistribution = totalDistribution + inputDistribution[a]
                
        #print ' totalDistribution', totalDistribution
        
        resultDistribution = []
        
        for a in range(0, len(inputDistribution)):
            if totalDistribution == 0:
                resultDistribution.append(0.0)
            else:
                resultDistribution.append(float(inputDistribution[a]) / float(totalDistribution))
                
        #print ' resultDistribution', resultDistribution
        
        return resultDistribution
                
# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------
    
def doTopicModeling(numberOfTopics, 
                        numberOfIterations, 
                        alpha, beta, 
                        pTextsWordTopicAssignments, 
                        pDistinctWordTopicCounts, 
                        pCorpusTopicCounts, 
                        pTextTopicCounts):
    
    textsWordTopicAssignments = pTextsWordTopicAssignments
    distinctWordTopicCounts = pDistinctWordTopicCounts
    corpusTopicCounts = pCorpusTopicCounts
    textTopicCounts = pTextTopicCounts
    
    for iteration in range(0, numberOfIterations):
        
        iterationStartTime = time.time()
        
        #print '\n iteration', iteration
        
        for text, wordTopicAssignments in textsWordTopicAssignments.iteritems():
            for wordTopicAssignment in wordTopicAssignments:
                
                word = wordTopicAssignment['word']
                oldTopic = wordTopicAssignment['topic']
                
                #print '\n', iteration, text, word, 'oldTopic', oldTopic
                #print ' BEFORE distinctWordTopicCounts[word]', distinctWordTopicCounts[word]
                #print ' BEFORE textTopicCounts[text]', textTopicCounts[text]
                #print ' BEFORE corpusTopicCounts', corpusTopicCounts
                
                distinctWordTopicCounts[word][oldTopic] = distinctWordTopicCounts[word][oldTopic] - 1
                textTopicCounts[text][oldTopic] = textTopicCounts[text][oldTopic] - 1
                corpusTopicCounts[oldTopic] = corpusTopicCounts[oldTopic] - 1
                
                #print ' SUBBED distinctWordTopicCounts[word]', distinctWordTopicCounts[word]
                #print ' SUBBED textTopicCounts[text]', textTopicCounts[text]
                #print ' SUBBED corpusTopicCounts', corpusTopicCounts
                
                #   ----------------------------------------------------
                #   A VERSION USING VECTORS OF WORD COUNTS.
                #   ----------------------------------------------------
                
                topicDistribution = initializeTopicCountArray(numberOfTopics)
                
                for a in range(0, numberOfTopics):
                    
                    topicDistribution[a] = (
                        (float(distinctWordTopicCounts[word][a]) + beta) *
                        (float(textTopicCounts[text][a]) + alpha) /
                        (float(corpusTopicCounts[a]) + beta)
                    )
                  
                topicDistribution = scaleDistributionTo1(topicDistribution)
                
                #   ----------------------------------------------------
                #   A VERSION USING DISTRIBUTIONS SUMMING TO ONE.
                #   DOESN'T SEEM TO WORK AS WELL AS THE VERSION USING
                #   WORD COUNTS.
                #   ----------------------------------------------------
                
                #distinctWordTopicCountsScaled = scaleDistributionTo1(distinctWordTopicCounts[word])
                #textTopicCountsScaled = scaleDistributionTo1(textTopicCounts[text])
                #corpusTopicCountsScaled = scaleDistributionTo1(corpusTopicCounts)
                
                #print '\n distinctWordTopicCountsScaled', distinctWordTopicCountsScaled
                #print ' textTopicCountsScaled', textTopicCountsScaled
                #print ' corpusTopicCountsScaled', corpusTopicCountsScaled
                
                #topicDistribution = initializeTopicCountArray(numberOfTopics)
                
                #for a in range(0, numberOfTopics):
                    
                #    topicDistribution[a] = (
                #        (float(distinctWordTopicCountsScaled[a]) + beta) *
                #        (float(textTopicCountsScaled[a]) + alpha) /
                #        (float(corpusTopicCountsScaled[a]) + beta)
                #    )
                  
                #topicDistribution = scaleDistributionTo1(topicDistribution)
                
                #print '\n topicDistribution', topicDistribution
                
                #   ----------------------------------------------------
                    
                r = random.random()
                        
                #print ' r', r
                
                index = 0
                while (r > 0):
                    r = r - topicDistribution[index]
                    if r > 0:
                        index = index + 1
                        
                newTopic = index
                        
                #print ' newTopic', newTopic
                
                distinctWordTopicCounts[word][newTopic] = distinctWordTopicCounts[word][newTopic] + 1
                textTopicCounts[text][newTopic] = textTopicCounts[text][newTopic] + 1
                corpusTopicCounts[newTopic] = corpusTopicCounts[newTopic] + 1
                
                #print ' AFTER distinctWordTopicCounts[word]', distinctWordTopicCounts[word]
                #print ' AFTER textTopicCounts[text]', textTopicCounts[text]
                #print ' AFTER corpusTopicCounts', corpusTopicCounts
                    
                wordTopicAssignment['topic'] = newTopic
        
        iterationStopTime = time.time()
        
        print 'iteration', iteration, "time", (iterationStopTime - iterationStartTime)
        
    return textsWordTopicAssignments, distinctWordTopicCounts, corpusTopicCounts, textTopicCounts
    
# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

if len(sys.argv) != 8:
    print 'USAGE: toyTopicModeller.py inputFolder numberOfTopics numberOfIterations alpha beta seed outputFolder'
    print len(sys.argv)
    sys.exit(2)

inputFolder = fixTrailingSlash(sys.argv[1])
numberOfTopics = int(sys.argv[2])
numberOfIterations = int(sys.argv[3])
alpha = float(sys.argv[4])
beta = float(sys.argv[5])
seed = int(sys.argv[6])
outputFolder = fixTrailingSlash(sys.argv[7])

print '\n inputFolder', inputFolder
print ' numberOfTopics', numberOfTopics
print ' numberOfIterations', numberOfIterations
print ' alpha', alpha
print ' beta', beta

random.seed(seed)
            
corpus = loadCorpus(inputFolder)

textsWordTopicAssignments, distinctWordTopicCounts, corpusTopicCounts, textTopicCounts = makeMatrices(corpus, numberOfTopics)

textsWordTopicAssignments, distinctWordTopicCounts, corpusTopicCounts, textTopicCounts = doTopicModeling(numberOfTopics, 
                                                                                                numberOfIterations, 
                                                                                                alpha, 
                                                                                                beta, 
                                                                                                textsWordTopicAssignments, 
                                                                                                distinctWordTopicCounts, 
                                                                                                corpusTopicCounts, 
                                                                                                textTopicCounts)
                                                                                                
outputStateFile(textsWordTopicAssignments, outputFolder)
