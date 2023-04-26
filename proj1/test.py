
import pandas as pd

#text='''downloads a vimeo channel """ downloads a vimeo channel """, downloads a vimeo url """'''
#text= ''' convert xml to url list """ convert xml to url list """, convert xml to url list """'''

class scoreTest():
    def __init__(self):
        self.filepath = ''
        self.BLEUList = []
        self.METEORList=[]

    def mean(self,List):
        return sum(List)/len(List)

    def run(self,path):
        self.filepath=path
        vpath = r"".join([self.filepath])
        df = pd.read_json(vpath, orient='records', lines=True)
        df=df[["score"]]
        i = 0
        set = 0
        thousand_count = 0
        print(len(df))
        print(df.mean(numeric_only=True))
        while set + i < len(df):
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            self.BLEUList.append(X[0][0])
            self.METEORList.append(X[0][1])
            # print(X[0])
            i=i+1

    def get_all_into_count(self):
        self.run('results/javaresult1.jsonl')
        #self.run('results/javaresult1.jsonl')
        print(self.mean(self.BLEUList))
        print(self.mean(self.METEORList))


class recordTest():
    def __init__(self, filepath='results/javaresult2_0.jsonl'):
        self.filepath = filepath

    def run(self):
        vpath = r"".join([self.filepath])
        df = pd.read_json(vpath, orient='records', lines=True)
        #df = df[["code","score"]]
        i = 0
        set = 0

        while set + i < 50:
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            print(X[0])
            print("Ref:\n"+X[2]+"\nSumm:\n"+X[3])
            print(X[4][0])
            print('\n\n')
            i = i + 1



#recordTest().run()
scoreTest().get_all_into_count()

#py1:
#0.08698681917211337
#0.12853877995642693
#py2:
#0.130077798632525
#0.18108317468829724

#java1:type3(is used to),del @
#0.03621800000000001
#0.073294

#java2:type3(used to),del @
#0.033362
#0.05708200000000001

#java3:type3,not del @
#0.041402
#0.078818
#0.10559973528069304
#0.16156063897763648