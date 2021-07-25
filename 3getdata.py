# coding=utf-8

#python 3getdata.py  ./data/data1234.xlsx ./data/data5.xlsx ./data_10_29/
#python 3getdata.py  ./data/data1234.xlsx ./data/data5.xlsx ./data_11_1/
from langconv import Converter
import pandas as pd
import csv
import math
import re
import argparse


def rmSymbol(sent):
    return re.sub("|／\n", "", sent)


'''
input : 4個同組的question
output : [[][]
          [][]
          [][]] 6個question pair
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

    #give number of negative sample   1 : 1000 => 6 * 1000 * 999 = 5994000
    #取1/3 = 1998000
    #取1/3 = 666000   這樣是6000 : 666000 = 1 : 100
    numOfNegSample = 1998000
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("input_file2")
    parser.add_argument("output_directory")
    args = parser.parse_args()

    data = pd.read_excel(args.input_file, sheet_name='Sheet1', header=0)
    data2 = pd.read_excel(args.input_file2, sheet_name='Sheet1', header=0)
    n = len(data)
    m = len(data2)

    # for index, row in data.iterrows():
    #     print(index)

    ##write data
    #https://github.com/google-research/bert/issues/593   no dev data is ok  do_eval = falser in .sh

    allGroup = []  #for negative sample
    with open(args.output_directory + '/train.csv','w', newline='', encoding="utf8") as tCSV, \
         open(args.output_directory + '/dev.csv','w', newline='', encoding="utf8") as dCSV:

        tCSVW = csv.writer(tCSV, lineterminator='\n')
        dCSVW = csv.writer(dCSV, lineterminator='\n')

        for i in range(0, n, 4):
            targetQuestion = data['正確標準問題'][i]

            curGroup = []
            for j in range(4):
                index = i + j
                curGroup.append(data['測試題'][index])
            allGroup.append(curGroup)

            #create QuestionPair
            combination = Combination()
            curQuestionPairs = combination.combine(curGroup, 4, 2)

            #add postitive Question pair to .csv
            for index, QuestionPair in enumerate(curQuestionPairs):
                tCSVW.writerow(
                    [1,
                     rmSymbol(QuestionPair[0]),
                     rmSymbol(QuestionPair[1])])

            #At last, add negative Question pair to .csv
            if i == n - 4:
                sample = 0
                for firstIndex in range(len(allGroup)):
                    for firstEle in range(4):
                        for secondIndex in range(firstIndex + 1, len(allGroup),
                                                 1):
                            for secondEle in range(4):
                                tCSVW.writerow([
                                    0,
                                    rmSymbol(allGroup[firstIndex][firstEle]),
                                    rmSymbol(allGroup[secondIndex][secondEle])
                                ])
                                sample = sample + 1
                                if sample == numOfNegSample:
                                    break
                            if sample == numOfNegSample:
                                break
                        if sample == numOfNegSample:
                            break
                    if sample == numOfNegSample:
                        break
    ##write to test.csv
    s = 0
    with open(args.output_directory + '/test.csv',
              'w',
              newline='',
              encoding="utf8") as testCSV:
        testCSVW = csv.writer(testCSV, lineterminator='\n')
        for i in range(m):
            for j in range(n):
                testCSVW.writerow(
                    [0, rmSymbol(data2['測試題'][i]),
                     rmSymbol(data['測試題'][j])])
            ##for 查看
            #     s = s + 1
            #     if s > 4002:
            #         break
            # if s > 4002:
            #     break