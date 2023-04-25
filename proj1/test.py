
import pandas as pd

#text='''downloads a vimeo channel """ downloads a vimeo channel """, downloads a vimeo url """'''
#text= ''' convert xml to url list """ convert xml to url list """, convert xml to url list """'''

class scoreTest():
    def __init__(self, filepath='D:/PyProjects/proj1/result2_python4.jsonl'):
        self.filepath = filepath
        self.BLEUList = []
        self.METEORList=[]

    def mean(self,List):
        return sum(List)/len(List)

    def run(self):
        vpath = r"".join([self.filepath])
        df = pd.read_json(vpath, orient='records', lines=True)
        df=df[["score"]]
        i = 0
        set = 0
        thousand_count = 0
        print(len(df))
        print(df.mean())
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
        self.run()
        self.filepath= "results/pythonresult2_2.jsonl"
        self.run()
        print(self.mean(self.BLEUList))
        print(self.mean(self.METEORList))


class recordTest():
    def __init__(self, filepath='results/javaresult0.jsonl'):
        self.filepath = filepath

    def run(self):
        vpath = r"".join([self.filepath])
        df = pd.read_json(vpath, orient='records', lines=True)
        #df = df[["code","score"]]
        i = 0
        set = 0

        while set + i < 100:
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            """
            print("Ref:\n"+X[2]+"\nSumm:\n"+X[3])
            print(X[4][0])
            print('\n\n')
            # print(X[0])
            """
            print("Ref:\n" + X[1] + "\nSumm:\n" + X[2])
            print(X[3][0])
            print('\n\n')
            print(X[0])
            i = i + 1



recordTest().run()
#0.08698681917211337
#0.12853877995642693

#0.13131659999999967
#0.18320156250000091
#0.130077798632525
#0.18108317468829724