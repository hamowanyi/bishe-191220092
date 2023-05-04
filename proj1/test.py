
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
        self.run('carrot_rubyresult2_0.jsonl')
        #self.run('results/javaresult1.jsonl')
        print(self.mean(self.BLEUList))
        print(self.mean(self.METEORList))


class recordTest():
    def __init__(self, filepath='carrot_rubyresult2_0.jsonl'):
        self.filepath = filepath

    def run(self):
        vpath = r"".join([self.filepath])
        df = pd.read_json(vpath, orient='records', lines=True)
        #df = df[["code","score"]]
        i = 0
        set = 0
        num=len(df)
        if num>50:
            num=50
        while set + i < num:
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            if X[1]>512:
                i=i+1
                continue
            '''if X[4][0]>0.05:
                i=i+1
                continue'''
            print(X[0])
            print("Ref:\n"+X[2]+"\nSumm:\n"+X[3])
            print(X[4][0])
            print('\n\n')
            i = i + 1


class codeTest():
    def __init__(self, filepath='dataset/python/test.jsonl'):
        self.filepath = filepath

    def run(self):
        vpath = r"".join([self.filepath])
        df = pd.read_json(vpath, orient='records', lines=True)
        df = df[["original_string","docstring"]]
        i = 0
        set = 0

        while set + i < 50:
            print(set + i)
            X = df.loc[set + i]
            X = X.values
            X.tolist()
            print("Code:\n"+X[0]+"\nRef:\n"+X[1])
            print('\n\n')
            i = i + 1



recordTest().run()
scoreTest().get_all_into_count()
#codeTest().run()

#py1:
#0.08698681917211337
#0.12853877995642693

#py2:final_1
#0.130077798632525
#0.18108317468829724
#py3 newtest:
#0.12441372838181906
#0.169677724896099
#py4 type2:
#0.13123749162086112
#0.18043821557849676

#javaresult2:final
#0.10559973528069304
#0.16156063897763648

#js1:(test)
#0.06693922819811621
#0.09570370707991528

#js2:(test2):final
#0.08099397999999966
#0.10897590000000022

#go1:
#0.053730965279487584
#0.09255812607732129

#php1:
#0.1430692521763932
#0.18717598116169834


#ruby1(type3,test)
#0.08411356066613801
#0.11523790642347337
#ruby2:(type3,test2):final
#0.09523090999999902
#0.12887691999999992