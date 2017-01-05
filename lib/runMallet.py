#!/usr/bin/python

import sys, codecs, re, os, commands, time, string, random, logging
    
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

def runSimplestMallet(textsFolder, resultsFolder, malletFolder, nbrMalletTopics, extraParms=None):

    logging.info("simplestTest nbrMalletTopics " + str(nbrMalletTopics))

    thisMalletResultsFolder = resultsFolder + str(nbrMalletTopics) + "/"

    os.mkdir(thisMalletResultsFolder)

    cmd = malletFolder + "bin/mallet import-dir --input '" + textsFolder + "' --output '" + thisMalletResultsFolder + "simplestTest.mallet' --keep-sequence"

    executeCommand(cmd)

    extraMalletParameters = ''
    if extraParms != None:
        extraMalletParameters = extraParms

    cmd = malletFolder + "bin/mallet train-topics --random-seed 1 --input '" + thisMalletResultsFolder + "simplestTest.mallet' --num-topics " + str(nbrMalletTopics) + " --output-state '" + thisMalletResultsFolder + "simplestTest.state.gz' --output-doc-topics '" + thisMalletResultsFolder + "simplestTest.doc.txt' --output-topic-keys '" + thisMalletResultsFolder + "simplestTest.txt' " + extraMalletParameters

    executeCommand(cmd)

    cmd = "gunzip '" + thisMalletResultsFolder + "simplestTest.state.gz' "

    executeCommand(cmd)

    cmd = "./scripts/reorderTopicsInDocFile.py '" + thisMalletResultsFolder + "simplestTest.doc.txt' '" + thisMalletResultsFolder + "simplestTest.doc.reordered.csv' "

    executeCommand(cmd)

    cmd = "./scripts/reorderSpreadsheet.py '" + thisMalletResultsFolder + "simplestTest.doc.reordered.csv' '" + thisMalletResultsFolder + "simplestTest.ordered.csv'"

    executeCommand(cmd)

    cmd = "export LANG=en_US.UTF-8; echo $LANG; java -classpath ./scripts/JavaUtilitiesForMallet.jar edu.wustl.artsci.hdw.ListWordsInTopics '" + thisMalletResultsFolder + "simplestTest.state' 100 1> '" + thisMalletResultsFolder + "simplestTest.topicWords.csv'"

    executeCommand(cmd)

    cmd = "./scripts/getMatrixFromDocFile.py '" + thisMalletResultsFolder + "simplestTest.doc.txt' "

    executeCommand(cmd)

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def runMalletAlpha(textsFolder, resultsFolder, malletFolder, nbrMalletTopics, useAlpha):

    logging.info("simplestTest nbrMalletTopics " + str(nbrMalletTopics))

    thisMalletResultsFolder = resultsFolder + str(nbrMalletTopics) + "_" + str(useAlpha) + "/"

    os.mkdir(thisMalletResultsFolder)

    cmd = malletFolder + "bin/mallet import-dir --input '" + textsFolder + "' --output '" + thisMalletResultsFolder + "simplestTest.mallet' --keep-sequence"

    executeCommand(cmd)

    alphaParameter = ""
    if useAlpha:
        #alphaParameter = " --alpha 0.0001 "
        alphaParameter = " --optimize-interval 10 --optimize-burn-in 10 "

    cmd = malletFolder + "bin/mallet train-topics --input '" + thisMalletResultsFolder + "simplestTest.mallet' --num-topics " + str(nbrMalletTopics) + " --output-state '" + thisMalletResultsFolder + "simplestTest.state.gz' --output-doc-topics '" + thisMalletResultsFolder + "simplestTest.doc.txt' --output-topic-keys '" + thisMalletResultsFolder + "simplestTest.txt' --random-seed 1 " + alphaParameter

    executeCommand(cmd)

    cmd = "gunzip '" + thisMalletResultsFolder + "simplestTest.state.gz' "

    executeCommand(cmd)

    cmd = "./scripts/reorderTopicsInDocFile.py '" + thisMalletResultsFolder + "simplestTest.doc.txt' '" + thisMalletResultsFolder + "simplestTest.doc.reordered.csv' "

    executeCommand(cmd)

    cmd = "./scripts/reorderSpreadsheet.py '" + thisMalletResultsFolder + "simplestTest.doc.reordered.csv' '" + thisMalletResultsFolder + "simplestTest.ordered.csv'"

    executeCommand(cmd)

    cmd = "export LANG=en_US.UTF-8; echo $LANG; java -classpath ./scripts/JavaUtilitiesForMallet.jar edu.wustl.artsci.hdw.ListWordsInTopics '" + thisMalletResultsFolder + "simplestTest.state' 100 1> '" + thisMalletResultsFolder + "simplestTest.topicWords.csv'"

    executeCommand(cmd)

    cmd = "./scripts/getMatrixFromDocFile.py '" + thisMalletResultsFolder + "simplestTest.doc.txt' "

    executeCommand(cmd)

# ----------------------------------------------------------------------
#
# ----------------------------------------------------------------------

def runMalletIterationsAlphaBeta(textsFolder, resultsFolder, malletFolder, nbrMalletTopics, seed, iterations, alpha, beta):

    logging.info("simplestTest nbrMalletTopics " + str(nbrMalletTopics))

    thisMalletResultsFolder = resultsFolder + str(nbrMalletTopics) + "/"

    os.mkdir(thisMalletResultsFolder)

    cmd = malletFolder + "bin/mallet import-dir --input '" + textsFolder + "' --output '" + thisMalletResultsFolder + "simplestTest.mallet' --keep-sequence"

    executeCommand(cmd) 

    cmd = malletFolder + "bin/mallet train-topics --input '" + thisMalletResultsFolder + "simplestTest.mallet' --num-topics " + str(nbrMalletTopics) + " --output-state '" + thisMalletResultsFolder + "simplestTest.state.gz' --output-doc-topics '" + thisMalletResultsFolder + "simplestTest.doc.txt' --output-topic-keys '" + thisMalletResultsFolder + "simplestTest.txt' --random-seed " + str(seed) + " --num-iterations " + str(iterations) + " --alpha " + str(alpha) + " --beta " + str(beta)

    executeCommand(cmd)

    cmd = "gunzip '" + thisMalletResultsFolder + "simplestTest.state.gz' "

    executeCommand(cmd)

    cmd = "./scripts/reorderTopicsInDocFile.py '" + thisMalletResultsFolder + "simplestTest.doc.txt' '" + thisMalletResultsFolder + "simplestTest.doc.reordered.csv' "

    executeCommand(cmd)

    cmd = "./scripts/reorderSpreadsheet.py '" + thisMalletResultsFolder + "simplestTest.doc.reordered.csv' '" + thisMalletResultsFolder + "simplestTest.ordered.csv'"

    executeCommand(cmd)

    cmd = "export LANG=en_US.UTF-8; echo $LANG; java -classpath ./scripts/JavaUtilitiesForMallet.jar edu.wustl.artsci.hdw.ListWordsInTopics '" + thisMalletResultsFolder + "simplestTest.state' 100 1> '" + thisMalletResultsFolder + "simplestTest.topicWords.csv'"

    executeCommand(cmd)

    cmd = "./scripts/getMatrixFromDocFile.py '" + thisMalletResultsFolder + "simplestTest.doc.txt' "

    executeCommand(cmd)



