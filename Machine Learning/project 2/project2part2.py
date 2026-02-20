import os
import string
import sys
import pandas as pd
import numpy as np
import sklearn.tree
import sklearn.metrics
import sklearn.ensemble
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

def get_hyperparam(trainFilePath, validFilePath):
    trainFrame = pd.read_csv(trainFilePath)
    validFrame = pd.read_csv(validFilePath)
    Xtrain = trainFrame.iloc[:, :500]
    Ytrain = trainFrame.iloc[:, 500]
    Xvalid = validFrame.iloc[:, :500]
    Yvalid = validFrame.iloc[:, 500]
    criterion = {"gini", "entropy", "log_loss"}
    splitter = {"best", "random"}
    max_depth = {3, 5, 7, 9, 11}
    best_accuracy = 0
    best_c = ""
    best_s = ""
    best_depth = -1
    for c in criterion:
        for s in splitter:
            for md in max_depth:
                clf = sklearn.tree.DecisionTreeClassifier(criterion=c, splitter=s, max_depth=md)
                clf.fit(Xtrain.to_numpy(), Ytrain.to_numpy())

                Ypred = clf.predict(Xvalid.to_numpy())
                accuracy = sklearn.metrics.accuracy_score(Yvalid, Ypred)
                if(accuracy > best_accuracy):
                    best_accuracy = accuracy
                    best_c = c
                    best_s = s
                    best_depth = md

    print(str(best_accuracy) + " " + best_c + " " + best_s + " " + str(best_depth))
    return best_c, best_s, best_depth

def decisionClassify(Xtrain, Xtest, Ytrain, Ytest, crit, split):
    clf = sklearn.tree.DecisionTreeClassifier(criterion=crit, splitter=split)
    clf.fit(Xtrain.to_numpy(), Ytrain.to_numpy())
    Ypred = clf.predict(Xtest.to_numpy())
    accuracy = sklearn.metrics.accuracy_score(Ytest, Ypred)
    #F1 = sklearn.metrics.f1_score(Ytest, Ypred)
    print(f"Accuracy: {accuracy:.6f}")
    #print(f"F1 score: {F1:.6f}")

def baggingClassify(Xtrain, Xtest, Ytrain, Ytest, crit, split):
    clf = sklearn.tree.DecisionTreeClassifier(criterion=crit, splitter=split)
    bag = sklearn.ensemble.BaggingClassifier(estimator=clf, n_estimators=25)
    bag.fit(Xtrain.to_numpy(), Ytrain.to_numpy())
    Ypred = bag.predict(Xtest.to_numpy())
    accuracy = sklearn.metrics.accuracy_score(Ytest, Ypred)
    #F1 = sklearn.metrics.f1_score(Ytest, Ypred)
    print(f"Accuracy: {accuracy:.6f}")
    #print(f"F1 score: {F1:.6f}")

def randomForestClassify(Xtrain, Xtest, Ytrain, Ytest, crit):
    rfc = sklearn.ensemble.RandomForestClassifier(criterion=crit,  n_estimators=100)
    rfc.fit(Xtrain.to_numpy(), Ytrain.to_numpy())
    Ypred = rfc.predict(Xtest.to_numpy())
    accuracy = sklearn.metrics.accuracy_score(Ytest, Ypred)
    #F1 = sklearn.metrics.f1_score(Ytest, Ypred)
    print(f"Accuracy: {accuracy:.6f}")
    #print(f"F1 score: {F1:.6f}")

def getGradientHyperparam(trainFilePath, validFilePath):
    trainFrame = pd.read_csv(trainFilePath)
    validFrame = pd.read_csv(validFilePath)
    Xtrain = trainFrame.iloc[:, :500]
    Ytrain = trainFrame.iloc[:, 500]
    Xvalid = validFrame.iloc[:, :500]
    Yvalid = validFrame.iloc[:, 500]
    loss = {"log_loss", "exponential"}
    learning_rate = {.1, .5, 1}
    criterion = {"friedman_mse"}
    best_accuracy = 0
    best_loss = ""
    best_learning_rate = 0
    best_c = ""
    for c in criterion:
        for l in loss:
            for n in learning_rate:
                clf = sklearn.ensemble.GradientBoostingClassifier(loss=l, criterion=c, learning_rate=n, n_estimators=25)
                clf.fit(Xtrain.to_numpy(), Ytrain.to_numpy())
                Ypred = clf.predict(Xvalid.to_numpy())
                accuracy = sklearn.metrics.accuracy_score(Yvalid, Ypred)
                if(accuracy > best_accuracy):
                    best_accuracy = accuracy
                    best_c = c
                    best_loss = l
                    best_learning_rate = n

    print(str(best_accuracy) + " " + best_loss + " " + best_c + " " + str(best_learning_rate))
   
    return best_loss, best_c, best_learning_rate

def gradientBoostClassify(Xtrain, Xtest, Ytrain, Ytest, l, c, n):
    gbc = sklearn.ensemble.GradientBoostingClassifier(loss=l, criterion=c, learning_rate=n, n_estimators=5)
    gbc.fit(Xtrain.to_numpy(), Ytrain.to_numpy())
    Ypred = gbc.predict(Xtest.to_numpy())
    accuracy = sklearn.metrics.accuracy_score(Ytest, Ypred)
    #F1 = sklearn.metrics.f1_score(Ytest, Ypred)
    print(f"Accuracy: {accuracy:.6f}")
    #print(f"F1 score: {F1:.6f}")


def main():
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True)
    X = X / 255.0 # Normalize pixel values to [0,1]
    # Split into training (60K) and test (10K) sets
    X_train, X_test = X[:60000], X[60000:]
    y_train, y_test = y[:60000], y[60000:]
    model = 0
    model = int(input("1. Decision Tree" + '\n' + "2. Bagging Decision Tree" + '\n' + "3.Random Forest Classifier" + '\n' + "4.Gradient boosting Classifier" + '\n'))
    while(model not in {1, 2, 3, 4}):
        model = int(input("Choose a valid model (1, 2, 3, 4)"))
    
    if(model == 1):
        #criterion, splitter, max_depth = get_hyperparam(trainFilePath, validFilePath)
        decisionClassify(X_train, X_test, y_train, y_test, "entropy", "random")
    elif(model == 2):
        #criterion, splitter, max_depth = get_hyperparam(trainFilePath, validFilePath)
        baggingClassify(X_train, X_test, y_train, y_test, "entropy", "random")
    elif(model == 3):
        #criterion, splitter, max_depth = get_hyperparam(trainFilePath, validFilePath)
        randomForestClassify(X_train, X_test, y_train, y_test, "log_loss")
    elif(model == 4):
        #loss, criterion, learning_rate = getGradientHyperparam(trainFilePath, validFilePath)
        gradientBoostClassify(X_train, X_test, y_train, y_test, "log_loss", "friedman_mse", 1)

if __name__ == "__main__":
    main()