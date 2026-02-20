#Project 1 for CS6375.001
#Pranith Mullapudi PXM220087

import os
import string
import sys
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

def getAllTrainFiles(targetFolder):
    trainFiles = []
    for root, folders, files in os.walk(targetFolder):
        for file in files:
            if file.endswith(".txt"):
                trainFiles.append(os.path.join(root, file))
    return trainFiles

def extractUniqueWords(files):
    stopWords = set(stopwords.words('english'))
    resultWords = set()
    for file in files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read().lower()
                    text = text.translate(str.maketrans('', '', string.punctuation))
                    words = word_tokenize(text)
                    filterWords = [w for w in words if w.isalpha() and w not in stopWords]
                    resultWords.update(filterWords)
    
    return sorted(resultWords)

def bernoulliRep(vocabulary, files):
    rows = []
    for file in files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            words = word_tokenize(text)
            row = {word: (1 if word in words else 0) for word in vocabulary}
            row['label'] = 1 if 'spam' in os.path.dirname(file) else 0
            rows.append(row)
    df = pd.DataFrame(rows, columns=vocabulary + ['label'])
    return df

def BoWRep(vocabulary, files):
    rows = []
    for file in files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            words = word_tokenize(text)
            row = {word: words.count(word) for word in vocabulary}
            row['label'] = 1 if 'spam' in os.path.dirname(file) else 0
            rows.append(row)
    df = pd.DataFrame(rows, columns=vocabulary + ['label'])
    return df



def main():
    nltk.download('stopwords') 
    nltk.download('punkt')

    chosenDataset = 0
    chosenDataset = int(input("Choose a dataset: 1, 2, 4" + '\n'))
    while(chosenDataset not in {1, 2, 4}):
        chosenDataset = int(input("Choose a valid dataset: 1, 2, 4" + '\n'))
    repType = -1
    repType = int(input("Choose a representation:" + '\n' + "0: Multinomial" + '\n' + "1: Bernoulli" + '\n'))
    while(repType not in {0, 1}):
        repType = int(input("Invalid choice, 0 or 1" + '\n'))

    representation = "multinomial" if repType == 0 else "bernoulli"
    print("Attempting to generate enron" + str(chosenDataset) + " dataset with " + str(representation) + " representation")
    trainFilePath = "./dataset/enron" + str(chosenDataset) + "/train"
    trainFiles = getAllTrainFiles(trainFilePath)
    if(len(trainFiles) == 0):
        sys.exit("Failed to obtain train data files")
    uniqueWords = set()
    uniqueWords = extractUniqueWords(trainFiles)
    print("Extracted unique words")
    testFilePath = "./dataset/enron" + str(chosenDataset) + "/test"
    testFiles = getAllTrainFiles(testFilePath)
    #At this point vocabulary is generated, Now need to Make the actual representation
    if repType == 1:
        trainDf = bernoulliRep(uniqueWords, trainFiles)
        testDf = bernoulliRep(uniqueWords, testFiles)
        trainDf.to_csv('csv/enron' + str(chosenDataset) + "_bernoulli_train", index=False)
        testDf.to_csv('csv/enron' + str(chosenDataset) + "_bernoulli_test", index=False)
    else:
        trainDf = BoWRep(uniqueWords, trainFiles)
        testDf = BoWRep(uniqueWords, testFiles)
        trainDf.to_csv('csv/enron' + str(chosenDataset) + "_bow_train", index=False)
        testDf.to_csv('csv/enron' + str(chosenDataset) + "_bow_test", index=False)
    print("Exported to csv file")

if __name__ == "__main__":
    main()

