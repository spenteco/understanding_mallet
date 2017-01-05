#!/usr/bin/python

import sys, codecs, re, os, commands, time, string, random, logging

import numpy as np
    
# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def generateZipfTopicsAndZ(topicsFolder, numberOfTopics, topicSize, nbrZwords):
    
    logging.info("generateZipfTopicsAndZ numberOfTopics " + str(numberOfTopics) + " topicSize " + str(topicSize) + "\n")
    
    endings = []
    for a in string.lowercase:
        for b in string.lowercase:
            for c in string.lowercase:
                endings.append(a + b + c)
    
    for a in range(0, numberOfTopics):
        
        topicLetter = string.uppercase[a]
        
        outF = codecs.open(topicsFolder + topicLetter + ".txt", "w", encoding="utf-8")
        
        for b in range(0, topicSize):
            outF.write(topicLetter + endings[b] + "\n")
            
        outF.close()   
        
    topicLetter = "Z"
    
    outF = codecs.open(topicsFolder + topicLetter + ".txt", "w", encoding="utf-8")
    
    #for b in range(0, (nbrZwords * 2)):
    for b in range(0, topicSize):
        outF.write(topicLetter + endings[b] + "\n")
        
    outF.close()   
    
# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def generateZipfTopics(topicsFolder, numberOfTopics, topicSize):
    
    logging.info("generateZipfTopics numberOfTopics " + str(numberOfTopics) + " topicSize " + str(topicSize) + "\n")
    
    endings = []
    for a in string.lowercase:
        for b in string.lowercase:
            for c in string.lowercase:
                endings.append(a + b + c)
    
    for a in range(0, numberOfTopics):
        
        topicLetter = string.uppercase[a]
        
        outF = codecs.open(topicsFolder + topicLetter + ".txt", "w", encoding="utf-8")
        
        for b in range(0, topicSize):
            outF.write(topicLetter + endings[b] + "\n")
            
        outF.close()     
    
# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def generateSimpleTopics(topicsFolder, numberOfTopics, topicSize):
    
    logging.info("generateSimpleTopics numberOfTopics " + str(numberOfTopics) + " topicSize " + str(topicSize) + "\n")
    
    endings = []
    for a in string.lowercase:
        for b in string.lowercase:
            for c in string.lowercase:
                endings.append(a + b + c)
    
    for a in range(0, numberOfTopics):
        
        topicLetter = string.uppercase[a]
        
        outF = codecs.open(topicsFolder + topicLetter + ".txt", "w", encoding="utf-8")
        
        for b in range(0, topicSize):
            outF.write(topicLetter + endings[b] + "\n")
            
        outF.close()

        

