# coding=utf-8
import numpy as np
import pandas as pd

numberOfTest = 1000
pathOfPred = "../z_predict/4.tsv"

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

threshold = 0.99

# 找每一組的首位(標準答案)的值  false negative
first = []
for i in range(len(groupRes)):
    for j in range(len(groupRes[i])):
        if j == 0:
            first.append(groupRes[i][j])
num = 0
for i in first:
    if i < threshold:
        print(i)
        num = num + 1
print("threshold %f" % threshold)
print("false negative %d" % num)

#找非首位的值 false positive
nonfirst = []
for i in range(len(groupRes)):
    for j in range(len(groupRes[i])):
        if j != 0:
            nonfirst.append(groupRes[i][j])
num = 0
for i in nonfirst:
    if i >= threshold:
        #print(i)
        num = num + 1
print("false positive : %d" % num)
