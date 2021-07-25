# coding=utf-8

#python 2getTrain.py  ./data/5000data.xlsx ./data10_26_750/
from langconv import Converter
import pandas as pd
import csv
import math
import re
import argparse


def rmSymbol(sent):
    return re.sub("|／\n", "", sent)


'''
input : 五個同組的question
output : [[][]
          [][]
          [][]] 10個question pair
'''


class Combination:
    def combine(self, text, n, k):
        res = []
        self.backtrack(text, n, k, res, [], 1)
        return res

    def backtrack(self, text, n, k, res, path, index):
        if len(path) == k:
            res.append(path)
            return
        for i in range(index, n + 1):
            self.backtrack(text, n, k, res, path + [text[i - 1]], i + 1)


if __name__ == '__main__':

    numOfNegSample = 4
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_directory")
    args = parser.parse_args()

    data = pd.read_excel(args.input_file, sheet_name='測試集', header=0)
    data2 = pd.read_excel(args.input_file, sheet_name='問題', header=0)
    n = len(data)  #5000 測試集內'測試題'與'正確標準問題'
    m = len(data2)  #1000 問題內 '標準問題'
    stdQuestion = data2['標準問題']  #All 標準問題  1000

    #決定negative sample 有多少 ：改成max
    perc = min(999, math.floor(len(stdQuestion) * 0.75))
    print("negative sample number %d" % perc)


    with open(args.output_directory + '/train.csv','w', newline='', encoding="utf8") as tCSV, \
         open(args.output_directory + '/dev.csv','w', newline='', encoding="utf8") as dCSV, \
             open(args.output_directory + '/test.csv','w', newline='', encoding="utf8") as testCSV:

        tCSVW = csv.writer(tCSV, lineterminator='\n')
        dCSVW = csv.writer(dCSV, lineterminator='\n')
        testCSVW = csv.writer(testCSV, lineterminator='\n')

        for i in range(0, n, 5):
            targetQuestion = data['正確標準問題'][i]
            otherQuestion = stdQuestion.loc[stdQuestion != targetQuestion]
            #make sure otherQuestion num == 999
            otherQuestion = otherQuestion.sample(n=perc)

            curGroup = []
            for j in range(5):
                index = i + j
                curGroup.append(data['測試題'][index])
            #create QuestionPair
            combination = Combination()
            curQuestionPairs = combination.combine(curGroup, 5, 2)
            #add postitive Question pair to .csv
            for index, QuestionPair in enumerate(curQuestionPairs):
                if index < 7:
                    tCSVW.writerow([
                        1,
                        rmSymbol(QuestionPair[0]),
                        rmSymbol(QuestionPair[1])
                    ])
                elif 7 <= index and index < 9:
                    dCSVW.writerow([
                        1,
                        rmSymbol(QuestionPair[0]),
                        rmSymbol(QuestionPair[1])
                    ])
                else:
                    #test data[0]為0
                    testCSVW.writerow([
                        0,
                        rmSymbol(QuestionPair[0]),
                        rmSymbol(QuestionPair[1])
                    ])

            #add negative sample to train.csv, dev.csv
            for negativeQuestion in otherQuestion.values:
                tCSVW.writerow(
                    [0,
                     rmSymbol(data['測試題'][i]),
                     rmSymbol(negativeQuestion)])
                dCSVW.writerow(
                    [0,
                     rmSymbol(data['測試題'][i]),
                     rmSymbol(negativeQuestion)])

            #add negative sample to test.csv(999個)，i為當前組index
            for index, row in enumerate(data['測試題']):
                if index != i and index % 5 == 0:
                    testCSVW.writerow([
                        0,
                        rmSymbol(data['測試題'][i + 3]),
                        rmSymbol(data['測試題'][index])
                    ])
