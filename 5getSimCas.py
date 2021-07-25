# coding=utf-8
#得到match schema2 繁簡增生

#QQ' 3個為training, 1個為dev, 1個為test
#test 為1000個一組 答案在第一個(0, 1001, 2001...)
#收集所有非正確Q', 從中選n個
#python3 4getdataQQ.py  ./data/5000data.xlsx ./data_12_11/
from langconv import Converter
import pandas as pd
import csv
import math
import re
import argparse


def simple2tradition(line):
    return Converter('zh-hant').convert(line)


def tradition2simple(line):
    return Converter('zh-hans').convert(line)


def rmSymbol(sent):
    return re.sub(" |／\n", "", sent)


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

    # perc = min(999, math.floor(len(stdQuestion) * 0.75))
    perc = min(999, 4)
    print("negative sample number %d" % perc)


    with open(args.output_directory + '/train.csv','w', newline='', encoding="utf8") as T_csv, \
         open(args.output_directory + '/dev.csv','w', newline='', encoding="utf8") as D_csv, \
             open(args.output_directory + '/test.csv','w', newline='', encoding="utf8") as testCSV:

        Tcsv_w = csv.writer(T_csv, lineterminator='\n')
        Dcsv_w = csv.writer(D_csv, lineterminator='\n')
        testCSVW = csv.writer(testCSV, lineterminator='\n')

        for i in range(0, n, 5):
            targetQuestion = data['正確標準問題'][i]
            otherQuestion = stdQuestion.loc[stdQuestion != targetQuestion]
            #make sure otherQuestion num == 999
            otherQuestionForTest = otherQuestion.sample(n=perc)
            otherQuestionForDev = otherQuestion.sample(n=perc)

            for j in range(5):
                index = i + j
                if index % 5 == 0 or index % 5 == 1 or index % 5 == 2:
                    Tcsv_w.writerow([
                        1,
                        tradition2simple(rmSymbol(data['測試題'][index])),
                        tradition2simple(rmSymbol(data['正確標準問題'][i]))
                    ])
                    Tcsv_w.writerow([
                        1,
                        tradition2simple(rmSymbol(data['測試題'][index])),
                        simple2tradition(rmSymbol(data['正確標準問題'][i]))
                    ])
                    Tcsv_w.writerow([
                        1,
                        simple2tradition(rmSymbol(data['測試題'][index])),
                        tradition2simple(rmSymbol(data['正確標準問題'][i]))
                    ])
                    Tcsv_w.writerow([
                        1,
                        simple2tradition(rmSymbol(data['測試題'][index])),
                        simple2tradition(rmSymbol(data['正確標準問題'][i]))
                    ])

                    # negative sample
                    for negativeQuestion in otherQuestionForTest.values:
                        Tcsv_w.writerow([
                            0,
                            tradition2simple(rmSymbol(data['測試題'][index])),
                            tradition2simple(rmSymbol(negativeQuestion))
                        ])
                        Tcsv_w.writerow([
                            0,
                            tradition2simple(rmSymbol(data['測試題'][index])),
                            simple2tradition(rmSymbol(negativeQuestion))
                        ])
                        Tcsv_w.writerow([
                            0,
                            simple2tradition(rmSymbol(data['測試題'][index])),
                            tradition2simple(rmSymbol(negativeQuestion))
                        ])
                        Tcsv_w.writerow([
                            0,
                            simple2tradition(rmSymbol(data['測試題'][index])),
                            simple2tradition(rmSymbol(negativeQuestion))
                        ])
                        # Tcsv_w.writerow([
                        #     0,
                        #     rmSymbol(negativeQuestion),
                        #     rmSymbol(data['測試題'][index])
                        # ])
                elif index % 5 == 3:
                    Dcsv_w.writerow([
                        1,
                        tradition2simple(rmSymbol(data['測試題'][index])),
                        tradition2simple(rmSymbol(data['正確標準問題'][i]))
                    ])
                    Dcsv_w.writerow([
                        1,
                        tradition2simple(rmSymbol(data['測試題'][index])),
                        simple2tradition(rmSymbol(data['正確標準問題'][i]))
                    ])
                    Dcsv_w.writerow([
                        1,
                        simple2tradition(rmSymbol(data['測試題'][index])),
                        tradition2simple(rmSymbol(data['正確標準問題'][i]))
                    ])
                    Dcsv_w.writerow([
                        1,
                        simple2tradition(rmSymbol(data['測試題'][index])),
                        simple2tradition(rmSymbol(data['正確標準問題'][i]))
                    ])

                    # if i < 1135:
                    #     Dcsv_w.writerow([
                    #         1,
                    #         tradition2simple(rmSymbol(data['測試題'][index])),
                    #         tradition2simple(rmSymbol(data['正確標準問題'][i]))
                    #     ])
                    #     Dcsv_w.writerow([
                    #         1,
                    #         tradition2simple(rmSymbol(data['正確標準問題'][i])),
                    #         tradition2simple(rmSymbol(data['測試題'][index]))
                    #     ])
                    # else:
                    #     Dcsv_w.writerow([
                    #         1,
                    #         simple2tradition(rmSymbol(data['測試題'][index])),
                    #         simple2tradition(rmSymbol(data['正確標準問題'][i]))
                    #     ])
                    #     Dcsv_w.writerow([
                    #         1,
                    #         simple2tradition(rmSymbol(data['正確標準問題'][i])),
                    #         simple2tradition(rmSymbol(data['測試題'][index]))
                    #     ])
                    # negative sample
                    for negativeQuestion in otherQuestionForDev.values:
                        Dcsv_w.writerow([
                            0,
                            tradition2simple(rmSymbol(data['測試題'][index])),
                            tradition2simple(rmSymbol(negativeQuestion))
                        ])
                        Dcsv_w.writerow([
                            0,
                            tradition2simple(rmSymbol(data['測試題'][index])),
                            simple2tradition(rmSymbol(negativeQuestion))
                        ])
                        Dcsv_w.writerow([
                            0,
                            simple2tradition(rmSymbol(data['測試題'][index])),
                            rmSymbol(negativeQuestion)
                        ])
                        Dcsv_w.writerow([
                            0,
                            simple2tradition(rmSymbol(data['測試題'][index])),
                            simple2tradition(rmSymbol(negativeQuestion))
                        ])
                        # Dcsv_w.writerow([
                        #     0,
                        #     rmSymbol(negativeQuestion),
                        #     rmSymbol(data['測試題'][index])
                        # ])
                else:  # 不需更改
                    testCSVW.writerow([
                        0,
                        rmSymbol(data['測試題'][index]),
                        rmSymbol(data['正確標準問題'][i])
                    ])
                    for negativeQuestion in otherQuestion.values:
                        testCSVW.writerow([
                            0,
                            rmSymbol(data['測試題'][index]),
                            rmSymbol(negativeQuestion)
                        ])