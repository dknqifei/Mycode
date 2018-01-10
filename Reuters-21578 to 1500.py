# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os 

os.chdir("E://python//reuters-data")

Data_dict = {}
"""first_time = True
for label in categories:
    if first_time:
        Data_sum = pd.read_csv(label+'.csv',index_col=0)
        first_time = False
    else:
        Data = pd.read_csv(label+'.csv',index_col=0)
        Data_sum = pd.concat([Data_sum,Data],axis = 1)
    print(Data_sum.shape)
    Data_sum.fillna(0,inplace = True)
    Data_sum = Data_sum.astype('int64')
    Data_sum.to_csv('sum.csv')
    """
    
#Data_sum = pd.read_csv('sum.csv',index_col=0)   

print(Data_sum.shape)
Data_rowsum = Data_sum.sum(axis = 1)
Data_sort = Data_rowsum.sort_values(ascending=False)
Data2000 = Data_sort.iloc[:2000]
Data_F = Data_sum.loc[Data2000.index,:]
Data_colsum = Data_F.sum(axis = 0)
Data_sort2 = Data_colsum.sort_values(ascending=False)
Data_gt_10 = Data_sort2[:-100]
Data_final = Data_F.loc[:,Data_gt_10.index]

Data_final.to_csv("reuters_data2000.csv")

