# -*- coding: utf-8 -*-

import nltk
import numpy as np
import pandas as pd
import re
from nltk.corpus import reuters 
#stopwords
from nltk.corpus import stopwords
from collections import Counter
import os
os.chdir("E://python//reuters-data")

#分句的pattern
pattern = r"""(?x)                   # set flag to allow verbose regexps 
              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
              |\.\.\.                # ellipsis 
              |(?:[.,;"'?():-_`])    # special characters with meanings 
            """  
            
#text = 'That U.S.A. poster-print costs $12.40...'
#a = nltk.regexp_tokenize(text, pattern)
cachedStopWords = stopwords.words("english")
cachedStopWords.append('lt')
cachedStopWords.append('gt')

#选出前 X 个categories以及对应的样本数
def topX_label(X):
    documents  = reuters.fileids()
    print(str(len(documents)) + " documents total")
    categories = reuters.categories()
    print(str(len(categories)) + " categories total")
    d = dict()
    for label in categories:
        data_cat = reuters.fileids(label)
        d[label] = len(data_cat)
    #print(d)
    d_sorted = sorted(d.items(), key = lambda i:i[1], reverse = True)
    #print(d_sorted[:X])
    top_label = list(map(lambda i:i[0] ,d_sorted[:X]))
    num_label = list(map(lambda i:i[1] ,d_sorted[:X]))
    return top_label, num_label

#把对应的raw 分词
def tokenize(text):
    min_length = 2
    words = map(lambda word:word.lower(), nltk.regexp_tokenize(text, pattern))
    words = [word for word in words
                  if word not in cachedStopWords]
    p = re.compile('[a-zA-Z]+');
    filtered_tokens =list(filter(lambda token:
                  p.match(token) and len(token)>=min_length,
         words));
    return filtered_tokens

k=0    

#还可以变快，比如连100个保存一下，最会concat起来
csv_shape=[]
categories, num_Categories = topX_label(10)
label = categories[4]
for label in categories:
    first_time = True
    documents_categories = reuters.fileids(label)
    for doc in documents_categories:
        k += 1
        text = reuters.raw(doc)
        words = tokenize(text)
        count_dict = Counter(words)
        doc_name = doc+'_'+label
        Vec = pd.Series(count_dict, dtype='int64', name = doc+'_'+label)
        if first_time:
            Data = Vec
            first_time = False
        else:
            Data = pd.concat([Data,Vec],axis = 1)
        print(label+'-'+str(k))
    k=0
    Data.fillna(0,inplace = True)
    Data.astype('int64')
    csv_shape.append(Data.shape)
    Data.to_csv(label+'.csv')
        
    #print(len(documents_categories))
    


