import csv

import pandas as pd
import jsonlines
import json
import torch
import torch.nn as nn
import torch.utils.data as Data
from prompt_base import Prompt_base
from pyspark.sql import SparkSession

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} device'.format(device))

class pythonTest():
    def __init__(self,filepath='D:/PyProjects/proj1/dataset/python/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath=filepath
        self.outputList=[]


    def run(self):
        vpath= r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i=0
        set=14000
        thousand_count=0
        print(len(df))
        pb_model=Prompt_base(tokenizer_str='Salesforce/codet5-large',model_str='Salesforce/codet5-large')
        while set+i <len(df):
            print(set+i)
            X=df.loc[set+i]
            X=X.values
            X.tolist()
            #print(X[0])
            self.outputList.append(pb_model.run([X[0],X[1]]))
            i=i+1
            if i==2000:
                i=0
                set=set+2000
                thousand_count=thousand_count+1
                self.savetoFile(thousand_count)

    def savetoFile(self,i):
        filename='result_third'+str(i)+'.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename,double_precision=4,orient='records',lines=True)

class javaTest():
    def __init__(self,filepath='D:/PyProjects/proj1/dataset/java/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath=filepath
        self.outputList=[]


    def run(self):
        vpath= r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i=0
        set=0
        thousand_count=0
        print(len(df))
        pb_model=Prompt_base(language='java',tokenizer_str='Salesforce/codet5-large',model_str='Salesforce/codet5-large')
        while set+i <len(df):
            print(set+i)
            X=df.loc[set+i]
            X=X.values
            X.tolist()
            #print(X[0])
            self.outputList.append(pb_model.run([X[0],X[1]]))
            i=i+1
            if i==2000:
                i=0
                set=set+2000
                thousand_count=thousand_count+1
                self.savetoFile(thousand_count)

    def savetoFile(self,i):
        filename='javaresult'+str(i)+'.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename,double_precision=4,orient='records',lines=True)
        
test1=javaTest()
test1.run()
test1.savetoFile(0)


