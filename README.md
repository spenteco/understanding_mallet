
understanding_mallet
====================

A collection of scripts for useful for learning about the [Mallet topic modeling toolkit](http://mallet.cs.umass.edu/).  I wrote these years ago, and I don't entirely recall all the details.  I ran a few of the scripts before putting them on github, and I've fairly sure that they'll run okay, but I'm not positive all of them will run.  Which shouldn't be a problem, since they aren't that complicated.

The basic idea here is: 1) generate topics, 2) generate texts from the topics; 3) topic model the texts; 4) examine the outputs from topic modeling to see how well or poorly topic modelling inferred the original topics.

The collection consists of:

**toyTopicModeller.py**, which is exactly what it sounds like.  It implements, as near as I was able, the process that [David Mimno outlined  in a 2012 talk at MITH](https://vimeo.com/53080123).  To run:

    USAGE: toyTopicModeller.py inputFolder numberOfTopics numberOfIterations alpha beta seed outputFolder

Caution: toyTopicModeller.py has not of Mallet's performance-improving goodies (hence, it's "toy-ness").  It's very slow.  So don't run it on a big corpus.

A bunch of scripts named like **mallet_test.N.py** which, with one exception, run Mallet using a number of different settings and inputs (the exception is mallet_test.6.py, which executes toyTopicModeller.py instead of Mallet).  These scripts take no command-line parameters; instead, their settings are coded as literals at the bottom of each script.

To run the mallet_test.N.py scripts, you'll need Mallet installed somewhere on your computer.  The path to the Mallet is part of the settings used to run the mallet_test.N.py scripts; see the bottom of each script for the places where you'll need to change the code to point to Mallet on your computer.

Each of the mallet_test.N.py scripts does more or less the same thing:

* It generates a set of topics.  Topics are composed of arbitrary four-letter words.  One topic consists of words with start with "A" (e.g, AAAA, AAAB, AAAC, etc); the next with words that start with B; and so forth.

* Then, using those topics, it generates a set of documents, building each document from a subset of the four-letter-word topics.  The point, of course, is that we know what words are in the topics, because we made both the words and topics, and we know what's in the documents, because we made them too.

* It runs topic modeling on the made-up documents consisting of four-letter words.

* It runs a couple of diagnostic reports which help me evaluate how well or poorly Mallet did at recovering the topics from the documents, all of which, plus the topics and texts, gets dump into the **testResults** folder, job-by-job.

Lastly, the **lib** folder contains bits and pieces used by the mallet_test.N.py scripts.

I never quite succeeded in generating a corpus which exhibits the same word-frequency and document-frequency distributions we see in the wild.  If there's a big to-do where, that's it.


diagnostic reports
==================

Each iteration of a **mallet_test.N.py** script produces a report with the following sections (this example comes from a run where the documents were made from 10 topics, and I requested that Mallet infer 10 topics).

These two sections show how many words from the made-up topics (a through z) ended up in each of Mallet's 10 topics (0 through 9).

    letters-topics topic       0      1      2      3      4      5      6      7      8      9
    letters-topics a          48     33     33     55      4     44   6036     14      5     27
    letters-topics b          30     16     17     17     37     22     10     62     40   6214
    letters-topics c          16     27   3797     66     45      3     14      9     19     37
    letters-topics d          22   5072     15      9     77     60     35     16     20     23
    letters-topics e          13     57     17      4   4297     15      6     25     18     31
    letters-topics f           4     36     45   4743      4     67     35      2     37      9
    letters-topics g          26     25     16      8     19     60     13   3197     54     64
    letters-topics h          18     20     40     42     34     31      7     33   5729     29
    letters-topics i          15     52      1     88     10   4257     30     58     25     13
    letters-topics j        4192     38     19      7      5      7     44     10     17     27

    letters-topics topic       a      b      c      d      e      f      g      h      i      j
    letters-topics 0          48     30     16     22     13      4     26     18     15   4192
    letters-topics 1          33     16     27   5072     57     36     25     20     52     38
    letters-topics 2          33     17   3797     15     17     45     16     40      1     19
    letters-topics 3          55     17     66      9      4   4743      8     42     88      7
    letters-topics 4           4     37     45     77   4297      4     19     34     10      5
    letters-topics 5          44     22      3     60     15     67     60     31   4257      7
    letters-topics 6        6036     10     14     35      6     35     13      7     30     44
    letters-topics 7          14     62      9     16     25      2   3197     33     58     10
    letters-topics 8           5     40     19     20     18     37     54   5729     25     17
    letters-topics 9          27   6214     37     23     31      9     64     29     13     27

    topic/document seg a    numberOfWords   6299 highTopic   6 highTopicNumberOfWords   6036 segregation 0.95
    topic/document seg b    numberOfWords   6465 highTopic   9 highTopicNumberOfWords   6214 segregation 0.96
    topic/document seg c    numberOfWords   4033 highTopic   2 highTopicNumberOfWords   3797 segregation 0.94
    topic/document seg d    numberOfWords   5349 highTopic   1 highTopicNumberOfWords   5072 segregation 0.94
    topic/document seg e    numberOfWords   4483 highTopic   4 highTopicNumberOfWords   4297 segregation 0.95
    topic/document seg f    numberOfWords   4982 highTopic   3 highTopicNumberOfWords   4743 segregation 0.95
    topic/document seg g    numberOfWords   3482 highTopic   7 highTopicNumberOfWords   3197 segregation 0.91
    topic/document seg h    numberOfWords   5983 highTopic   8 highTopicNumberOfWords   5729 segregation 0.95
    topic/document seg i    numberOfWords   4549 highTopic   5 highTopicNumberOfWords   4257 segregation 0.93
    topic/document seg j    numberOfWords   4366 highTopic   0 highTopicNumberOfWords   4192 segregation 0.96

An overall accuracy score:

    topic-document okayWords (unique) 9029 0.879933729656
    topic-document problemWords (unique) 1232 0.120066270344

Sections which report the accuracy of words, depending on how many documents the words appear in.  Low document-frequency words have a poor accuracy:

    topic-document frequency accuracy rate

     freq  words  error   rate
        1    496    315   0.36
        2   1234    359   0.70
        3   1854    235   0.87
        4   2068    135   0.93
        5   1769     78   0.95
        6   1231     50   0.95
        7    699     42   0.93
        8    352     12   0.96
        9    135      4   0.97
       10     45      2   0.95
       11     14      0   1.00
       12      5      0   1.00
       13      3      0   1.00

I have no idea what this section is

    document/topic seg 0    numberOfWords   4384 highLetter   j highLetterNumberOfWords   4192 segregation 0.95
    document/topic seg 1    numberOfWords   5376 highLetter   d highLetterNumberOfWords   5072 segregation 0.94
    document/topic seg 2    numberOfWords   4000 highLetter   c highLetterNumberOfWords   3797 segregation 0.94
    document/topic seg 3    numberOfWords   5039 highLetter   f highLetterNumberOfWords   4743 segregation 0.94
    document/topic seg 4    numberOfWords   4532 highLetter   e highLetterNumberOfWords   4297 segregation 0.94
    document/topic seg 5    numberOfWords   4566 highLetter   i highLetterNumberOfWords   4257 segregation 0.93
    document/topic seg 6    numberOfWords   6230 highLetter   a highLetterNumberOfWords   6036 segregation 0.96
    document/topic seg 7    numberOfWords   3426 highLetter   g highLetterNumberOfWords   3197 segregation 0.93
    document/topic seg 8    numberOfWords   5964 highLetter   h highLetterNumberOfWords   5729 segregation 0.96
    document/topic seg 9    numberOfWords   6474 highLetter   b highLetterNumberOfWords   6214 segregation 0.95

An overall accuracy score, again, but flipped for some reason (I wrote this code several years ago, and I've forgotten why some things are the way the are):

    document-topic okayWords (unique) 9029 0.879933729656
    document-topic problemWords (unique) 1232 0.120066270344

    topic-document frequency accuracy rate

     freq  words  error   rate
        1    496    315   0.36
        2   1234    359   0.70
        3   1854    235   0.87
        4   2068    135   0.93
        5   1769     78   0.95
        6   1231     50   0.95
        7    699     42   0.93
        8    352     12   0.96
        9    135      4   0.97
       10     45      2   0.95
       11     14      0   1.00
       12      5      0   1.00
       13      3      0   1.00

    overall accuracy 0.774283368586
