# coding=utf-8
import numpy as np
import pandas as pd

numberOfTest = 1000
pathOfPred = "../z_predict/500.tsv"

res = []
groupRes = []
predictionAnsIndex = []
with open(pathOfPred, 'r') as f:
    for line in f.readlines():
        prob = line.split('\t')[1]
        res.append(float(prob))

#get predictionIndex
for i in range(0, len(res), numberOfTest):
    groupRes.append(res[i:i + numberOfTest])
for i in range(len(groupRes)):
    maxValue = 0
    index = 0
    for j in range(len(groupRes[i])):
        if maxValue < groupRes[i][j]:
            index = j + i * numberOfTest
            maxValue = groupRes[i][j]
    predictionAnsIndex.append(index)

#計算acc : 答案為0, 1000, 2000...
wrongPrediction = []
wrongCnt = 0
for predictionIndex in predictionAnsIndex:
    if predictionIndex % 1000 != 0:
        wrongCnt = wrongCnt + 1
        wrongPrediction.append(predictionIndex)
acc = (numberOfTest - wrongCnt) / numberOfTest

print("accuracy = %f" % acc)
# print(wrongPrediction)
# print(len(wrongPrediction))