# coding=utf-8

#python 3getdataEveryGroup.py  ./data/data1234.xlsx ./data/data5.xlsx ./data_11_4/
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
    numOfNegSample = 666000
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("input_file2")
    parser.add_argument("output_directory")
    args = parser.parse_args()

    data = pd.read_excel(args.input_file, sheet_name='Sheet1', header=0)
    data2 = pd.read_excel(args.input_file2, sheet_name='Sheet1', header=0)
    n = len(data)
    m = len(data2)
    #n = 4000
    #5% 會生成neg數量：60,0000 == (4000 * 0.05 = 200) * 3 * 1000
    #2% 會生成neg數量：24,0000 == (4000 * 0.02 = 80) * 3 * 1000.   但dev為 * 4 * 1000 = 32000
    #0.2% 會生成neg數量：2,4000 == (4000 * 0.002 = 8) * 3 * 1000
    #0.2% 會生成neg數量：1,2000
    #0.00025 總共生成4000(每一個問題類一個)
    perc = min(3996, math.floor(n * 0.001))
    print("negative sample number %d" % perc)

    allGroup = []  #for negative sample
    with open(args.output_directory + '/train.csv','w', newline='', encoding="utf8") as tCSV, \
         open(args.output_directory + '/dev.csv','w', newline='', encoding="utf8") as dCSV:

        tCSVW = csv.writer(tCSV, lineterminator='\n')
        dCSVW = csv.writer(dCSV, lineterminator='\n')

        for i in range(0, n, 4):
            curGroup = []
            for j in range(4):
                index = i + j
                curGroup.append(data['測試題'][index])
            allGroup.append(curGroup)

            #create QuestionPair
            combination = Combination()
            curQuestionPairs = combination.combine(curGroup, 3, 2)

            #add postitive Question pair to .csv
            for index, QuestionPair in enumerate(curQuestionPairs):
                tCSVW.writerow(
                    [1,
                     rmSymbol(QuestionPair[0]),
                     rmSymbol(QuestionPair[1])])
            #add postitive Question pair to .dev
            for k in range(0, 3, 1):
                dCSVW.writerow(
                    [1, rmSymbol(curGroup[3]),
                     rmSymbol(curGroup[k])])

            #At last, add negative Question pair to .csv
            if i == n - 4:
                for firstIndex in range(len(allGroup)):
                    otherData = data[
                        data['正確標準問題'] != data['正確標準問題'][firstIndex * 4]]
                    otherQuestion = otherData['測試題']
                    for firstEle in range(3):
                        otherQuestion = otherQuestion.sample(n=perc)
                        for negativeQuestion in otherQuestion.values:
                            tCSVW.writerow([
                                0,
                                rmSymbol(allGroup[firstIndex][firstEle]),
                                rmSymbol(negativeQuestion)
                            ])
                    for firstEleForDev in range(4):
                        otherQuestionForDev = otherQuestion.sample(n=perc)
                        for negativeQuestionForDev in otherQuestionForDev.values:
                            dCSVW.writerow([
                                0,
                                rmSymbol(allGroup[firstIndex][firstEleForDev]),
                                rmSymbol(negativeQuestionForDev)
                            ])
    ##write to test.csv
    # s = 0
    # with open(args.output_directory + '/test.csv',
    #           'w',
    #           newline='',
    #           encoding="utf8") as testCSV:
    #     testCSVW = csv.writer(testCSV, lineterminator='\n')
    #     for i in range(m):
    #         for j in range(n):
    #             testCSVW.writerow(
    #                 [0, rmSymbol(data2['測試題'][i]),
    #                  rmSymbol(data['測試題'][j])])

    ##for 查看
    #     s = s + 1
    #     if s > 4002:
    #         break
    # if s > 4002:
    #     break
