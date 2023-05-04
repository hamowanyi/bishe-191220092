import pandas as pd
import jsonlines
import json
import torch
import torch.nn as nn
import torch.utils.data as Data
from prompt_base import Prompt_base
from transformers import AutoTokenizer, AutoModelWithLMHead,T5ForConditionalGeneration


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

    def run(self,_t,_m,set=0,end=-1,skip=1,type=0):#set=n*2000
        vpath= r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i=0
        thousand_count=0
        print(len(df))
        pb_model=Prompt_base(language='python',skipTokens=skip,_tokenizer=_t,_model=_m,_promptType=type)
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
        filename='carrot_pythonresult2_'+str(i)+'.jsonl'
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

    def run(self,_t,_m,set=0,end=-1,skip=1,type=0):
        vpath= r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i=0
        thousand_count=0
        print(len(df))
        pb_model=Prompt_base(language='java',skipTokens=skip,_tokenizer=_t,_model = _m,_promptType=type)
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
        filename='carrot_javaresult1_'+str(i)+'.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename,double_precision=4,orient='records',lines=True)


class jsTest():
    def __init__(self, filepath='dataset/javascript/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath = filepath
        self.outputList = []

    def run(self,_t,_m, set=0, end=-1,skip=1,type=0):
        vpath = r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i = 0
        thousand_count = 0
        print(len(df))
        pb_model = Prompt_base(language='js',skipTokens=skip,_tokenizer=_t,_model=_m,_promptType=type)
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
        filename = 'carrot_jsresult1_' + str(i) + '.jsonl'
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

    def run(self,_t,_m, set=0, end=-1,skip=1,type=0):
        vpath = r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i = 0
        thousand_count = 0
        print(len(df))
        pb_model = Prompt_base(language='go', skipTokens=skip,_tokenizer=_t,_model=_m,_promptType=type)
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
        filename = 'carrot_goresult1_' + str(i) + '.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename, double_precision=4, orient='records', lines=True)


class phpTest():
    def __init__(self, filepath='dataset/php/test.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath = filepath
        self.outputList = []

    def run(self,_t,_m, set=0, end=-1,skip=1,type=0):
        vpath = r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i = 0
        thousand_count = 0
        print(len(df))
        pb_model = Prompt_base(language='php', skipTokens=skip,_tokenizer=_t,_model=_m,_promptType=type)
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
        filename = 'carrot_phpresult1_' + str(i) + '.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename, double_precision=4, orient='records', lines=True)


class rubyTest():
    def __init__(self, filepath='dataset/ruby/test2.jsonl'):
        '''with open(filepath, "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                print(item)
            f.close()
        '''
        self.filepath = filepath
        self.outputList = []

    def run(self,_t,_m, set=0, end=-1,skip=1,type=0):
        vpath = r"".join([self.filepath])
        data = pd.read_json(vpath, orient='records', lines=True)
        df = data[["code", "docstring"]]
        i = 0
        thousand_count = 0
        print(len(df))
        pb_model = Prompt_base(language='ruby', skipTokens=skip,_tokenizer=_t,_model=_m,_promptType=type)
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
        filename = 'carrot_rubyresult2_' + str(i) + '.jsonl'
        df = pd.DataFrame(self.outputList)
        df.to_json(filename, double_precision=4, orient='records', lines=True)


tk = AutoTokenizer.from_pretrained("codeparrot/codeparrot")
md = AutoModelWithLMHead.from_pretrained("codeparrot/codeparrot")
#tk=AutoTokenizer.from_pretrained("Salesforce/codet5-large")
#md=T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large")
#test1=pythonTest()
#test1.run(end=50,_t=tk,_m=md,skip=2)
#test1=javaTest()
#test1.run(end=50,_t=tk,_m=md,skip=2)
#test1=jsTest()
#test1.run(end=50,_t=tk,_m=md,skip=2)
#test1=goTest()
#test1.run(end=50,_t=tk,_m=md,skip=2)
test1=phpTest()
test1.run(end=50,_t=tk,_m=md,skip=2)
test1=rubyTest()
test1.run(end=50,_t=tk,_m=md,skip=2)