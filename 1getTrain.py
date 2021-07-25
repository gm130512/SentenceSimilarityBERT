# coding=utf-8
from langconv import Converter
import pandas as pd
import csv
import xlrd
import math

import re
import argparse


def rmSymbol(sent):
    return re.sub("|／\n", "", sent)


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
    perc = min(numOfNegSample, math.floor(len(stdQuestion) * 0.1))



    with open(args.output_directory + '/train.csv','w', newline='', encoding="utf8") as tCSV, \
         open(args.output_directory + '/dev.csv','w', newline='', encoding="utf8") as dCSV:

        tCSVW = csv.writer(tCSV, lineterminator='\n')
        dCSVW = csv.writer(dCSV, lineterminator='\n')

        for i in range(int(n * 0.8)):
            # curCustomer = data['客戶'][i]
            targetQuestion = data['正確標準問題'][i]
            otherQuestion = stdQuestion.loc[stdQuestion != targetQuestion]
            otherQuestion = otherQuestion.sample(n=perc)

            if i % 5 != 0:
                # Q' Q(origin)
                tCSVW.writerow(
                    [1,
                     rmSymbol(data['測試題'][i]),
                     rmSymbol(data['正確標準問題'][i])])
                #negative sample
                # for negetiveQuestion in otherQuestion.values:
                #     tCSVW.writerow([
                #         0,
                #         rmSymbol(data['測試題'][i]),
                #         rmSymbol(negetiveQuestion)
                #     ])
            # write to dev
            else:
                dCSVW.writerow(
                    [1,
                     rmSymbol(data['測試題'][i]),
                     rmSymbol(data['正確標準問題'][i])])
                # for negativeQuestion in otherQuestion.values:
                #     dCSVW.writerow([
                #         0,
                #         rmSymbol(data['測試題'][i]),
                #         rmSymbol(negetiveQuestion)
                #     ])
