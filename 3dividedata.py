import argparse
import pandas as pd
#python 3dividedata.py  ./data/5000data.xlsx ./data/5_18/
#python 3dividedata.py  ./data/2345data.xlsx ./data/5_18/

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_directory")
    args = parser.parse_args()

    df = pd.read_excel(args.input_file, sheet_name='測試集', header=0)
    # data1 = pd.read_excel(args.input_file, sheet_name='測試集', header=0)
    data = df.iloc[lambda x: x.index % 5 == 0]
    # data = df.iloc[lambda x: x.index % 4 != 3]
    # data1 = data1.iloc[lambda x: x.index % 5 == 0]
    # print(data1)

    data.to_excel('./data/5_18/data1.xlsx')
    # data1.to_excel('data5.xlsx')

    # print(row['學號'], row['姓名'])
    # old = list(row['姓名'])
    # old[1] = 'O'
    # newString = "".join(old)
    # f.write(row['學號'] + " " + newString + '\n')