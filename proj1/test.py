'''from transformers import AutoTokenizer, T5ForConditionalGeneration

tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large")

text=''''''
text=text.replace('\n','\r\n')
print(text+'\n\n')
input_ids = tokenizer(text, return_tensors="pt").input_ids

# simply generate a single sequence
generated_ids = model.generate(input_ids, max_length=25)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
'''
import method as mth
import pandas as pd
'''
def denoise(result, type=0):
    sList = mth.string_split(result)
    result = max(sList, key=len, default='')

    if len(result) <= 2:
        result = 'No valid comments generated'
    i0 = 0
    while result[i0] == ' ' and i0 < len(result):
        i0 = i0 + 1
    if i0 < len(result):
        result = result[i0:]
    if result.find('.') != -1:
        sList = result.split('.')
        result = max(sList, key=len, default='')
    if result.find(' is ') != -1:
        result = result[result.find('is'):]

    result_denoised = result
    return result_denoised
'''
#text='''downloads a vimeo channel """ downloads a vimeo channel """, downloads a vimeo url """'''
#text= ''' convert xml to url list """ convert xml to url list """, convert xml to url list """'''

class javaTest():
    def __init__(self, filepath='D:/PyProjects/proj1/result_third1.jsonl'):
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
        self.filepath='D:/PyProjects/proj1/result4.jsonl'
        self.run()
        self.filepath='D:/PyProjects/proj1/result_second3.jsonl'
        self.run()
        print(self.mean(self.BLEUList))
        print(self.mean(self.METEORList))

javaTest().get_all_into_count()
#0.08698681917211337
#0.12853877995642693