import pandas as pd
import jsonlines
import json
import torch
import torch.nn as nn
import torch.utils.data as Data
from prompt_base import Prompt_base

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} device'.format(device))

class pythonTest():
    def __init__(self,filepath='dataset/python/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath=filepath
        self.outputList=[]

    def run(self,set=0,end=-1):#set=n*2000
        vpath= r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i=0
        thousand_count=0
        print(len(df))
        pb_model=Prompt_base(tokenizer_str='Salesforce/codet5-large',model_str='Salesforce/codet5-large')
        if end==-1:
            end=len(df)
        while set+i <end:
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
        self.savetoFile(0)
    def savetoFile(self,i):
        filename='result2_python'+str(i)+'.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename,double_precision=4,orient='records',lines=True)

class javaTest():
    def __init__(self,filepath='dataset/java/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath=filepath
        self.outputList=[]

    def run(self,set=0,end=-1):
        vpath= r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i=0
        thousand_count=0
        print(len(df))
        pb_model=Prompt_base(language='java',tokenizer_str='Salesforce/codet5-large',model_str='Salesforce/codet5-large',skipTokens=False)
        if end==-1:
            end=len(df)
        while set+i <end:
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
        self.savetoFile(0)
    def savetoFile(self,i):
        filename='javaresult2_'+str(i)+'.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename,double_precision=4,orient='records',lines=True)


class jsTest():
    def __init__(self, filepath='dataset/javascript/test2.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath = filepath
        self.outputList = []

    def run(self, set=0, end=-1):
        vpath = r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i = 0
        thousand_count = 0
        print(len(df))
        pb_model = Prompt_base(language='js', tokenizer_str='Salesforce/codet5-large',
                               model_str='Salesforce/codet5-large', skipTokens=False)
        if end == -1:
            end = len(df)
        while set + i < end:
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            self.outputList.append(pb_model.run([X[0], X[1]]))
            i = i + 1
            if i == 2000:
                i = 0
                set = set + 2000
                thousand_count = thousand_count + 1
                self.savetoFile(thousand_count)
        self.savetoFile(0)

    def savetoFile(self, i):
        filename = 'jsresult2_' + str(i) + '.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename, double_precision=4, orient='records', lines=True)


class goTest():
    def __init__(self, filepath='dataset/go/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath = filepath
        self.outputList = []

    def run(self, set=0, end=-1):
        vpath = r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i = 0
        thousand_count = 0
        print(len(df))
        pb_model = Prompt_base(language='go', tokenizer_str='Salesforce/codet5-large',
                               model_str='Salesforce/codet5-large', skipTokens=False)
        if end == -1:
            end = len(df)
        while set + i < end:
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            self.outputList.append(pb_model.run([X[0], X[1]]))
            i = i + 1
            if i == 2000:
                i = 0
                set = set + 2000
                thousand_count = thousand_count + 1
                self.savetoFile(thousand_count)
        self.savetoFile(0)

    def savetoFile(self, i):
        filename = 'goresult1_' + str(i) + '.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename, double_precision=4, orient='records', lines=True)


test1=goTest()
test1.run()


