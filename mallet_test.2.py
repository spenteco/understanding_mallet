#!/usr/bin/python

import sys, codecs, re, os, commands, time, string, random, logging

from lib.generateTopics import *
from lib.generateTexts import *
from lib.runMallet import *
    
#-----------------------------------------------------------------------
#
#-----------------------------------------------------------------------

def executeCommand(cmd):

    logging.info(cmd + "\n")

    results = commands.getoutput("export PYTHONIOENCODING=UTF-8; " + cmd)

    logging.info(results + "\n")
    
    return results

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

def runZipfTest(testNbr, testRun, numberOfTopics, topicSize, numberOfTexts, sizeOfTexts, lowNbrTopics, highNbrTopics, malletTopicsNbrs, testResultsFolder, malletFolder):
        
    #
    #   SET UP THE RUN
    #
    
    thisTestFolder = fixTrailingSlash(testResultsFolder) + str(testNbr) + "/"
    thisRunFolder = fixTrailingSlash(testResultsFolder) + str(testNbr) + "/" + str(testRun) + "/"
    topicsFolder = fixTrailingSlash(testResultsFolder) + str(testNbr) + "/" + str(testRun) + "/topics/"
    textsFolder = fixTrailingSlash(testResultsFolder) + str(testNbr) + "/" + str(testRun) + "/texts/"
    resultsFolder = fixTrailingSlash(testResultsFolder) + str(testNbr) + "/" + str(testRun) + "/results/"
    
    try:
        os.mkdir(thisTestFolder)
    except OSError:
        noop = 0
    
    try:
        os.mkdir(thisRunFolder)
    except OSError:
        message = "ERROR: folder exists: " + thisTestFolder
        print message
    
    try:
        os.mkdir(topicsFolder)
    except OSError:
        message = "ERROR: folder exists: " + thisTestFolder
        print message
    
    try:
        os.mkdir(textsFolder)
    except OSError:
        message = "ERROR: folder exists: " + thisTestFolder
        print message
    
    try:
        os.mkdir(resultsFolder)
    except OSError:
        message = "ERROR: folder exists: " + thisTestFolder
        print message
        
    logging.basicConfig(filename=thisTestFolder + "testLog." + str(testNbr) + ".txt", level=logging.INFO, format='%(message)s')
    
    message = "Running test " + str(testNbr) + " run " + str(testRun) + "\n"
    print message
    logging.info(message)
    
    message = "thisTestFolder " + thisTestFolder
    print message
    logging.info(message)
    
    message = "thisRunFolder " + thisRunFolder
    print message
    logging.info(message)
    
    message = "topicsFolder " + topicsFolder
    print message
    logging.info(message)
    
    message = "textsFolder " + textsFolder
    print message
    logging.info(message)
    
    message = "resultsFolder " + resultsFolder + "\n"
    print message
    logging.info(message)
    
    
    #
    #   TOPIC AND TEXT GENERATION
    #
    
    generateZipfTopics(topicsFolder, numberOfTopics, topicSize)
    
    generateZipfTexts(textsFolder, topicsFolder, numberOfTexts, sizeOfTexts, lowNbrTopics, highNbrTopics)
    
    #
    #   RUN MALLET
    #
    
    for nbrMalletTopics in malletTopicsNbrs:
        
        runSimplestMallet(textsFolder, resultsFolder, fixTrailingSlash(malletFolder), nbrMalletTopics)
    
    #
    #   RUN DIAGNOSTICS
    #

    cmd = "./lib/documentFrequency.py '" + textsFolder + "'  > '" + resultsFolder + "simplestTest." + str(testNbr) +  ".documentFrequency.txt'"

    executeCommand(cmd)
    
    for nbrMalletTopics in malletTopicsNbrs:

        thisMalletResultsFolder = resultsFolder + str(nbrMalletTopics) + "/"

        cmd = "./lib/stateReport.py '" + thisMalletResultsFolder + "simplestTest.state' '" + resultsFolder + "simplestTest." + str(testNbr) +  ".documentFrequency.txt' > '" + thisTestFolder + "simplestTest." + str(testNbr) +  "." + str(testRun) + "." + str(nbrMalletTopics) + ".stateReport.txt'"

        executeCommand(cmd)
    
    
# ----------------------------------------------------------------------
#   runZipfTest(testNbr, testRun, numberOfTopics, topicSize, 
#       numberOfTexts, sizeOfTexts, lowNbrTopics, highNbrTopics, 
#       [malletTopicsNbrs], testResultsFolder, malletFolder)
# ----------------------------------------------------------------------

runZipfTest(2, 1, 10, 1000, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 2, 10, 1000, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 3, 10, 1000, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 4, 10, 1000, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 5, 10, 1000, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")

#runZipfTest(2, 6, 10, 500, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 7, 10, 500, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 8, 10, 500, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 9, 10, 500, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 10, 10, 500, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")

#runZipfTest(2, 11, 10, 250, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 12, 10, 250, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 13, 10, 250, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 14, 10, 250, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")
#runZipfTest(2, 15, 10, 250, 50, 1000, 2, 5, [5,10,20], "testResults", "/home/spenteco/0/mallet-2.0.7")

