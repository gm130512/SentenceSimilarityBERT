# coding=utf-8
import numpy as np
import pandas as pd

target = pd.read_excel("./data/5000data.xlsx", sheet_name="測試集")
test_client = "客戶F"
test_target = target[target["客戶"] == test_client]
#index : 1135
#print(test_target.iloc[0]["測試題"])

#is_next_sim :  分數的list
is_next_sim = []
maxLine = 1546000  ##分兩次，因為list放不下。         773個選正確答案
with open("../catch/test_results.tsv", 'r') as fd:
    i = 0
    #max : 226,5603    300,0000個分兩次做
    for line in fd:
        i = i + 1
        if (i <= maxLine):
            tmp = line.strip('\n ')
            if tmp != "":
                prob = tmp.split('\t')[1]
                is_next_sim.append(float(prob))
    fd.close()
#print(is_next_sim[0:10])

test_sent_pair = pd.read_csv("../catch/test.csv", header=None, nrows=maxLine)
test_sent_pair.columns = ["sim_prob", "Q", "Q'"]

test_sent_pair["sim_prob"] = is_next_sim
# print(test_sent_pair.iloc[0:3])
#    sim_prob           Q                                  Q'
# 0  0.000029  “挥卡”和刷卡一样吗  16周岁以上18周岁以下在柜面办理开卡、书面挂失、卡片激活需要的手续
# 1  0.000014  “挥卡”和刷卡一样吗                         16岁以下公民办理开户
# 2  0.000015  “挥卡”和刷卡一样吗               ATM他行转账撤销后，款项需要多久退回账户
#################################################################
#做n個，每個有773個元素的陣列 : 放每一個問題的所有分數
a = test_sent_pair["sim_prob"].values.reshape(-1, 773)
#做n個，每個有773個元素的陣列 : 放每一個問題的所有分數 和 問題，標準問題
b = test_sent_pair.values.reshape(-1, 773, 3)

#test_pred : 把每一個問題 做predict的結果放進來
test_pred = []
#print(a.shape) : (2000, 773)。 a.shape[0] = 2000
for i in range(a.shape[0]):
    #max_id : 最大值的index
    max_id = a[i].argmax()
    pred = b[i][max_id][2]
    test_pred.append(pred)

# test_Q : 測試的所有問題(type : list)         一次處理2000個
test_Q = test_sent_pair['Q'].unique().tolist()

test_t = []
i = 0
for q in test_Q:
    i = i + 1
    if i == 291:
        print(q)  #test_target(read_csv)內有空格，q(test data.csv)內沒空格
        tmp = test_target[test_target["測試題"] == q]["正確標準問題"].iloc[0]
        print(test_target["測試題"])
        print(type(test_target["測試題"]))
    # test_t.append(tmp)

# ac = (np.array(test_pred) == np.array(test_t))
# ac.sum() / ac.shape[0]