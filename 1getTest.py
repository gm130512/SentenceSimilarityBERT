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

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_directory")
    args = parser.parse_args()

    data = pd.read_excel(args.input_file, sheet_name='測試集', header=0)
    data2 = pd.read_excel(args.input_file, sheet_name='問題', header=0)
    n = len(data)  #5000 測試集內'測試題'與'正確標準問題'
    m = len(data2)  #1000 問題內 '標準問題'
    stdQuestion = data2['標準問題']  #All 標準問題  1000

    # 5000 * 0.2 * 1000 = 100,0000
    with open(args.output_directory + '/test.csv',
              'w',
              newline='',
              encoding="utf8") as testCSV:

        testCSVW = csv.writer(testCSV, lineterminator='\n')
        for i in range(int(n * 0.8), n, 1):
            customerQuestion = data['測試題'][i]
            for j in range(m):
                testCSVW.writerow(
                    [0,
                     rmSymbol(customerQuestion),
                     rmSymbol(stdQuestion[j])])
