#Project 1 for CS6375.001
#Pranith Mullapudi PXM220087
import os
import string
import sys
import time
import numpy as np
import pandas as pd

def main():
    chosenDataset = 0
    chosenDataset = int(input("Choose a dataset: 1, 2, 4" + '\n'))
    while(chosenDataset not in {1, 2, 4}):
        chosenDataset = int(input("Choose a valid dataset: 1, 2, 4" + '\n'))
    repType = -1
    repType = int(input("Choose a representation:" + '\n' + "0: Multinomial" + '\n' + "1: Bernoulli" + '\n'))
    while(repType not in {0, 1}):
        repType = int(input("Invalid choice, 0 or 1" + '\n'))
    modelType = -1
    modelType = int(input("Choose a model" + '\n' + "0: Multinomial" + '\n' + "1: Bernoulli" + '\n' + "2: LogReg" + '\n'))
    while(modelType not in {0, 1, 2}):
        modelType = int(input("Must choose between 0, 1, and 2" + '\n'))
    if(repType == 0 and modelType == 1): #Ruling out combinations that don't work
        print("Cannot run Bernoulli model on BoW representation, exiting...")
        sys.exit(0)
    elif(repType == 1 and modelType == 0):
        print("Cannot run Multinomial model on Bernoulli representation, exiting...")
        sys.exit(0)
    else:
        if(modelType == 0 and repType == 0):
            V, log_prior, log_conditionalProb = trainMultinomial(chosenDataset)
            resultFrame = multinomialPredictions(chosenDataset, V, log_prior, log_conditionalProb)
            assessPerformance(resultFrame, modelType, repType, chosenDataset)
        elif(modelType == 1 and repType == 1):
            V, log_prior, log_cond_present, log_cond_absent = trainBernoulli(chosenDataset)
            resultFrame = bernoulliPredictions(chosenDataset, V, log_prior, log_cond_present, log_cond_absent)
            assessPerformance(resultFrame, modelType, repType, chosenDataset)
        else:
            resultFrame = LogisticRegression(chosenDataset, repType, .1, 5000) #Decided to combine train and predict for this since predict is such a small step
            assessPerformance(resultFrame, modelType, repType, chosenDataset)

        


def trainMultinomial(dataset):
    trainFrame = pd.read_csv('csv/enron' + str(dataset) + "_bow_train")
    #Setting up inputs for calculations
    X_train = trainFrame.drop(columns=["label"])
    y_train = trainFrame["label"]
    V = X_train.columns.values.tolist() #Peudo-step 1
    C = [0, 1] #Already know only two classes, if there were more could use a function to generalize to >2 classes
    N = len(trainFrame) #Peudo-step 2
    log_prior = {}
    log_conditionalProb = {t: {} for t in V}
    for c in C: #Peudo-step 3
        classDocuments = trainFrame[y_train == c]#Storing in a seperate df for step 6
        Nc = len(classDocuments) #Peudo-step 4
        log_prior[c] = np.log(Nc/N) #Peudo-step 5
        textConcat = classDocuments.drop(columns="label").sum(axis=0)
        totalTokens = textConcat.sum() #for Sigma Tct
        for t in V:
            log_conditionalProb[t][c] = np.log((textConcat[t] + 1)/(totalTokens + 1))
    return V, log_prior, log_conditionalProb
            
def multinomialPredictions(dataset, V, log_prior, log_conditionalProb):
    testFrame = pd.read_csv('csv/enron' + str(dataset) + "_bow_test")
    y_true = testFrame["label"]
    X_test = testFrame.drop(columns=["label"])
    C = [0, 1]
    predictions = []

    for index, row in X_test.iterrows():
        d = row.to_dict() #Extract datapoint
        W = [t for t in V if d.get(t, 0) > 0] #Only sum for words that are in the datapoint
        score = {}
        for c in C:
            s = log_prior[c] #start with prior
            for t in W: #for each word
                count = d.get(t, 0) 
                s += count * log_conditionalProb[t][c] #add count of words * conditional prob
            score[c] = s 
        predictions.append(max(score, key=score.get)) 
    testFrame["predicted"] = predictions #Add predictions next to true to compare
    return testFrame #Return and use as input in assessment function

def trainBernoulli(dataset): #Copy paste of multinomial training with few tweaks
    trainFrame = pd.read_csv('csv/enron' + str(dataset) + "_bernoulli_train")
    #Setting up inputs for calculations
    X_train = trainFrame.drop(columns=["label"])
    y_train = trainFrame["label"]
    V = X_train.columns.values.tolist() 
    C = [0, 1] 
    N = len(trainFrame) 
    log_prior = {}
    log_conditionalProb_present = {t: {} for t in V} #storing both so that I don't have to leave log space later
    log_conditionalProb_absent = {t: {} for t in V}
    for c in C: 
        classDocuments = trainFrame[y_train == c]
        Nc = len(classDocuments) 
        log_prior[c] = np.log(Nc/N) 
        for t in V:
            numWithT = (classDocuments[t] > 0).sum() 
            prob = (numWithT + 1)/(Nc + 2)
            log_conditionalProb_present[t][c] = np.log(prob)
            log_conditionalProb_absent[t][c] = np.log(1 - prob)

    return V, log_prior, log_conditionalProb_present, log_conditionalProb_absent
            
def bernoulliPredictions(dataset, V, log_prior, log_conditionalProb_present, log_conditionalProb_absent):
    testFrame = pd.read_csv('csv/enron' + str(dataset) + "_bernoulli_test")
    y_true = testFrame["label"]
    X_test = testFrame.drop(columns=["label"])
    C = [0, 1]
    predictions = []

    for index, row in X_test.iterrows():
        d = row.to_dict() #Extract datapoint
        score = {}
        for c in C:
            s = log_prior[c] #start with prior
            for t in V: #for each word in overall vocal since we count absence
                if d.get(t, 0) > 0: #if it appears or not 
                    s += log_conditionalProb_present[t][c] #add log(P(t | c))
                else: #if word isn't there
                    s += log_conditionalProb_absent[t][c] #add log(1-p(t | c))
            score[c] = s 
        predictions.append(max(score, key=score.get)) 
    testFrame["predicted"] = predictions #Add predictions next to true to compare
    return testFrame #Return and use as input in assessment function
    
def LogisticRegression(dataset, repType, learnRate, iterations): 
    rep = ["_bow_", "_bernoulli_"] #Since LR can be on either
    trainFrame = pd.read_csv('csv/enron' + str(dataset) + rep[repType] + "train")
    chosenLambda = chooseLambda(trainFrame, learnRate, iterations) #calling a helper method for chosing lambda 
    #Already made the chosenLambda method so this will be almost identical except for using the true training and test sets
    testFrame = pd.read_csv("csv/enron" + str(dataset) + rep[repType] + "test")
    XTrain = trainFrame.drop(columns=["label"]).to_numpy()
    YTrain = trainFrame["label"].to_numpy()
    XTest = testFrame.drop(columns=["label"]).to_numpy() #Converting to numpy arrays and splitting the features and labels
    YTest = testFrame["label"].to_numpy()   
    XTrain = np.hstack([np.ones((XTrain.shape[0], 1)), XTrain]) #Adding a column of ones at the front for the bias term
    XTest = np.hstack([np.ones((XTest.shape[0], 1)), XTest])  
    d, n = XTrain.shape #d feature vectors with n features each
    w = np.zeros(n)
    print("Performing training with chosen lambda")
    for i in range(iterations):
        z = np.dot(XTrain, w)
        result = sigmoid(z) #making the prediction with current weights
        gradient = (1/d) * np.dot(XTrain.T, (YTrain - result)) #avg of train transpose dot error (true value - result)
        gradient[1:] -= (chosenLambda/d) * w[1:] #Subtracting regularization from each column except bias
        w += learnRate * gradient #Update rule
    #At this point we have final weight vector w to make predictions with
    predictions = (sigmoid(np.dot(XTest, w)) >= 0.5).astype(int)
    testFrame["predicted"] = predictions
    return testFrame

def chooseLambda(trainFrame, learnRate, iterations): #May take direct iteration input or feed true iterations and use a fraction for tuning
    print("Beginning lambda tuning")
    lambdaSpace = [.001, .01, .1, 1, 10] #List of lamda's to try
    bestAccuracy = 0
    bestLambda = 0
    tuneTrainFrame = trainFrame.sample(frac=0.70) #split 70% of train into tuneing train
    tuneTestFrame = trainFrame.drop(tuneTrainFrame.index) #Rest 30% go into tuning test
    XTrain = tuneTrainFrame.drop(columns=["label"]).to_numpy()
    YTrain = tuneTrainFrame["label"].to_numpy()
    XTest = tuneTestFrame.drop(columns=["label"]).to_numpy()
    YTest = tuneTestFrame["label"].to_numpy()
    #sepearting them and also converting to numpy arrays to make sure dot products work
    XTrain = np.hstack([np.ones((XTrain.shape[0], 1)), XTrain]) #Adding a column of ones at the front for the bias term
    XTest = np.hstack([np.ones((XTest.shape[0], 1)), XTest])  
    d, n = XTrain.shape #d samples with n features each
    for l in lambdaSpace:
        print("Testing lambda " + str(l))
        w = np.zeros(n) #reset the weight vector
        for i in range(iterations/5): 
            z = np.dot(XTrain, w)
            result = sigmoid(z) #making the prediction with current weights
            gradient = (1/d) * np.dot(XTrain.T, (YTrain - result)) #avg of train transpose dot error (true value - result)
            gradient[1:] -= (l/d) * w[1:] #Subtracting regularization from each column except bias
            w += learnRate * gradient #Update rule
        #Time to evaluate this lambda's performace
        predictions = sigmoid(np.dot(XTest, w)) >= .5 #using where weights predicts test to be >= .5 
        accuracy = np.mean(predictions == YTest) #number of correct predictions over total
        if accuracy > bestAccuracy:
            bestAccuracy = accuracy
            bestLambda = l
    print("Choosing Lambda " + str(bestLambda))
    return bestLambda

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def assessPerformance(testFrame, model, repType, dataset): #Model and reptype just for printing in report
    correctFrame = testFrame["label"] == testFrame["predicted"]
    correctCount = correctFrame.sum() #since trues are 1's
    totalCount = len(testFrame)
    accuracy = correctCount/totalCount
    correctSpam = testFrame[(testFrame["label"] == 1) & (testFrame["predicted"] == 1)]
    correctSpamCount = len(correctSpam)
    totalSpam = (testFrame["label"] == 1).sum() 
    precision = correctSpamCount / (testFrame["predicted"] == 1).sum()
    recall = correctSpamCount / totalSpam
    F1Score = 2 * precision * recall / (precision + recall)
    models = ["Multinomial Naive Bayes", "Bernoulli Naive Bayes", "Logistic Regression"]
    reps = ["Bag of Words", "Bernoulli"]
    print("Results for " + models[model] + " on " + reps[repType] + " for dataset " + str(dataset))
    print(f"Accuracy: {accuracy:.6f}")
    print(f"Precision: {precision:.6f}")
    print(f"Recall: {recall:.6f}")
    print(f"F1 Score: {F1Score:.6f}")
    

if __name__ == "__main__":
    main()
