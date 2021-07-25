# coding=utf-8
import numpy as np
import pandas as pd

numberOfTest = 1000
pathOfPred = "../z_predict/test_results.tsv"
#
#get testQuestion
#get correctAns
#
testQuestion = []
correctAns = []
target = pd.read_excel("./data/5000data.xlsx", sheet_name="測試集")
with open("./data/test.csv", 'r') as f:
    i = 0
    for line in f.readlines():
        if (i % numberOfTest) == 0:
            q = line.split(',')[1]
            testQuestion.append(q)
        i = i + 1

for q in testQuestion:
    row = target[target['測試題'] == q]
    ans = row.iloc[0][2]
    correctAns.append(ans)

#
#get predictionAnsIndex
#
res = []
groupRes = []
predictionAnsIndex = []
with open(pathOfPred, 'r') as f:
    for line in f.readlines():
        prob = line.split('\t')[1]
        res.append(float(prob))
#1000 '正確標準答案'        0~999, 1000~1999
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

#print(predictionAnsIndex[0])

#
#get prediction 標準問題
#
predictionAns = []
target2 = pd.read_excel("./data/5000data.xlsx", sheet_name="問題")
for i in predictionAnsIndex:
    index = i % numberOfTest
    ans = target2.iloc[index][1]
    predictionAns.append(ans)

#
#計算acc
#
correctPrediction = 0
testWithWrongPrediction = []  #哪一題預測錯
wrongPrediction = []  #這題預測什麼東西出來
for i in range(len(predictionAns)):
    if predictionAns[i] == correctAns[i]:
        correctPrediction = correctPrediction + 1
    else:
        testWithWrongPrediction.append(testQuestion[i])
        wrongPrediction.append(predictionAns[i])
acc = correctPrediction / numberOfTest
print(acc)
