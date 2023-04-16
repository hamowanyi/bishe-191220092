import re

from transformers import AutoTokenizer, T5ForConditionalGeneration
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
import torch
import pandas as pd
import jsonlines
import json
import torch.nn as nn
import torch.utils.data as Data


class Prompt_base():
    def __init__(self,tokenizer_str='Salesforce/codet5-large',model_str='Salesforce/codet5-large',language='python',test=False):
        self.text=''
        self.input_size=0
        self.reference=[]
        self.tokenizer=AutoTokenizer.from_pretrained(tokenizer_str)
        self.model=T5ForConditionalGeneration.from_pretrained(model_str)
        self.result=''
        self.result_standardized=''
        self.score={}
        self.test=test
        self.language=language
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def all_block(self,str,c=' '):
        if len(str)>=2:
            str=str[1:len(str)]
        else:
            return True
        for i in range(len(str)):
            if str[i]!=c:
                return False
        return True

    def find_all(self,string, sub,beg=0,end=0):
        if end==0:
            end=len(string)
        string=string[beg:end]
        start = 0
        pos = []
        while True:
            start = string.find(sub, start)
            if start == -1:
                return pos
            pos.append(start)
            start += len(sub)

    def string_split(self,str):
        return re.split("[,*#'./\"\n(){}+-=_@!><&]", str)

    def code_preprocess_python(self,code):
        sum_symbol = '''"""'''

        #code=code.replace('\n','\r\n')
        pos = self.find_all(code, sum_symbol)
        #maybe have sum:
        if len(pos)>1:
            replaceList=[]
            i=0
            # record begin_position of sum
            while i < len(pos)-1:
                i1=pos[i]-1
                while i1 >= 0:
                    if code[i1]==' ':
                        i1=i1-1
                    else:
                        break
                if code[i1]=='\n':
                    replaceList.append([i1+1,pos[i+1]+2])
                    i=i+2
                else:
                    i=i+1
            i= len(replaceList)-1
            #del sum
            while i >=0:
                id=replaceList[i]
                if(id[1]<len(code)-1):
                    code=code[:id[0]]+code[id[1]+1:]
                else:
                    code=code[:id[0]]
                i-=1

        pos = self.find_all(code, '#')

        if len(pos) >= 1:
            replaceList = []
            i = 0
            # record begin_position of sum
            while i < len(pos):
                i1 = pos[i] - 1
                while i1 >= 0:
                    if  code[i1] == ' ':
                        i1 = i1 - 1
                    else:
                        break
                i2=i1+1
                while i2<len(code):
                    if code[i2] != '\n':
                        i2=i2+1
                    else:
                        break
                replaceList.append([i1 + 1, i2-1])
                i = i + 1
            i = len(replaceList) - 1
            # del sum
            while i >= 0:
                id = replaceList[i]
                if (id[1] < len(code) - 1):
                    code = code[:id[0]] + code[id[1] + 1:]
                else:
                    code = code[:id[0]]
                i -= 1

        #print(code)
        #del blocks
        pos=self.find_all(code,'\n')
        replaceList=[]
        i=0
        for i in range(len(pos)-1):
            if self.all_block(code[pos[i]:pos[i+1]]):
                replaceList.append(pos[i+1])
        i=len(replaceList)-1
        while i>=0:
            code=code[:replaceList[i]]+code[replaceList[i]+1:]
            i=i-1

        return code

    def set_prompt_python(self,code,type=1):
        if type==0:
            code = code + '''\n\n""" This function'''
        elif type==1:
            replaceID=code.find('\n')+1
            count=0
            while replaceID<len(code):
                if code[replaceID] == ' ':
                    count = count + 1
                    replaceID=replaceID+1
                else:
                    break
            blocks=''
            for i in range(count):
                blocks=blocks+' '
            if replaceID<len(code):
                code=code[:replaceID]+'''""" function to<extra_id_0>\n'''+blocks+code[replaceID:]
        elif type==2:
            replaceID = code.find('\n') + 1
            count = 0
            while replaceID < len(code):
                if code[replaceID] == ' ':
                    count = count + 1
                    replaceID = replaceID + 1
                else:
                    break
            blocks = ''
            for i in range(count):
                blocks = blocks + ' '
            if replaceID < len(code):
                code = code[:replaceID] + '''# function to<extra_id_0>\n''' + blocks + code[replaceID:]

        code = code.replace('\n', '\r\n')
        return code

    def code_preprocess_java(self,code):
        sum_symbol = '/*'
        pos = self.find_all(code, sum_symbol)
        #maybe have sum:
        if len(pos)>=1:
            replaceList=[]
            i_head=0
            while i_head<len(pos):
                i_tail = code.find('*/',pos[i_head]+2)
                if i_tail!=-1:
                    replaceList.append([pos[i_head],i_tail+1])
                else:
                    break
                i_head=i_head+1

            # record begin_position of sum
            i= len(replaceList)-1
            #del sum
            while i >=0:
                id=replaceList[i]
                if(id[1]<len(code)-1):
                    code=code[:id[0]]+code[id[1]+1:]
                else:
                    code=code[:id[0]]
                i-=1

        pos = self.find_all(code, '//')
        # maybe have //:
        if len(pos) >= 1:
            replaceList = []
            i = 0
            # record begin_position of sum
            while i < len(pos):
                i1 = pos[i] - 1
                while i1 >= 0:
                    if code[i1] == ' ':
                        i1 = i1 - 1
                    else:
                        break
                i2=i1+1
                while i2<len(code):
                    if code[i2] != '\n':
                        i2=i2+1
                    else:
                        break
                replaceList.append([i1 + 1, i2-1])
                i = i + 1
            i = len(replaceList) - 1
            # del sum
            while i >= 0:
                id = replaceList[i]
                if (id[1] < len(code) - 1):
                    code = code[:id[0]] + code[id[1] + 1:]
                else:
                    code = code[:id[0]]
                i -= 1

        #del blocks
        pos=self.find_all(code,'\n')
        replaceList=[]
        i=0
        for i in range(len(pos)-1):
            if self.all_block(code[pos[i]:pos[i+1]]):
                replaceList.append(pos[i+1])
        i=len(replaceList)-1
        while i>=0:
            code=code[:replaceList[i]]+code[replaceList[i]+1:]
            i=i-1

        return code

    def set_prompt_java(self,code,type=1):
        if type==0:
            code = code + '''\n\n/*method to'''
        elif type==1:
            replaceID=code.find('\n')+5
            if replaceID<len(code):
                code=code[:replaceID]+'''/*method to<extra_id_0>\n    '''+code[replaceID:]
        elif type==2:
            replaceID = code.find('\n') + 5
            if replaceID < len(code):
                code = code[:replaceID] + '''//used to<extra_id_0>\n    ''' + code[replaceID:]
        elif type==3:
            code='''/*method to<extra_id_0>\n'''+code
        code = code.replace('\n', '\r\n')
        return code

    def denoise(self,result,type=0):
        sList = self.string_split(result)
        #print(sList)
        result = max(sList, key=len, default='')
        #print("first result: "+result)
        sList = result.split('  ')

        if len(result)<=2:
            result='No valid comments generated'
        i0=0
        while i0<len(result) :
            if result[i0] == ' ':
                i0=i0+1
            else:
                break
        if i0<len(result):
            result=result[i0:]
        if result.find('.') != -1:
            sList = result.split('.')
            result = max(sList, key=len, default='')
        if result.find(' is ')!= -1:
            result=result[result.find(' is '):]

        result_denoised=result
        return result_denoised

    def standardize(self,result):
        #print(1)
        result_denoise = result
        tmp = result_denoise.find('  ')
        while tmp != -1:
            result_denoise = result_denoise.replace('  ', ' ', 1)
            tmp = result_denoise.find('  ')
        #print(2)
        result_denoise = result_denoise.replace('.','')
        result_denoise = result_denoise.replace('\n', '').replace('\r', '')
        result_denoise = result_denoise.replace('is a function that ', '')
        result_denoise = result_denoise.replace('is a function to ', '')
        result_denoise = result_denoise.replace('This function ', '')
        result_denoise = result_denoise.replace('The function ', '')
        #print(3)
        #print(result_denoise)


        if len(result_denoise)<=2:
            result_denoise='No valid comments generated'
        strFirst = result_denoise[0]
        result_denoise = result_denoise[1:]
        strFirst = strFirst.upper()
        result_denoise = strFirst + result_denoise + '.'
        return result_denoise

    def model_run(self):
        input_ids = self.tokenizer(self.text, return_tensors="pt").input_ids
        self.input_size=len(input_ids[0])
        if torch.cuda.is_available():
            input_ids=input_ids.cuda()
        generated_ids = self.model.generate(input_ids, max_length=25)
        self.result=self.tokenizer.decode(generated_ids[0],skip_special_tokens=True)

    def run(self,input):
        self.text=input[0]
        self.reference.clear()
        preprocess_ref = input[1]
        if self.language=='java' and input[1].find('@')!=-1:
            preprocess_ref=input[1][:input[1].find('@')]
            if len(preprocess_ref)==0:
                preprocess_ref=input[1]

        self.reference.append(preprocess_ref)
        if not self.test:
            #print('Origin:\n'+self.text)
            if self.language=='python':
                self.text=self.code_preprocess_python(self.text)
                self.text=self.set_prompt_python(self.text)
            elif self.language=='java':
                self.text = self.code_preprocess_java(self.text)
                self.text = self.set_prompt_java(self.text)
        #print('Preprocess:\n'+self.text)


        #Move to GPU and get result
        self.model_run()
        #print('Origin result: '+self.result)


        #Result denoise:
        result_denoised=self.denoise(self.result)
        #print('Denoised result: '+result_denoised)
        #Result standardizate:
        self.result_standardized=self.standardize(result_denoised)
        #print('Final result: '+self.result_standardized)


        #BLEU-4 and METEOR:
        ref=[]
        for i in range(len(self.reference)):
            ref_tmp=self.reference[i].split()
            ref.append(ref_tmp)
        can=self.result_standardized.split()
        SF=SmoothingFunction()
        self.score["BLEU-4"]=sentence_bleu(ref,can,smoothing_function=SF.method2)
        self.score["METEOR"]=meteor_score(ref,can)
        #print(self.score)
        return {"code": self.text, "reference": self.reference[0], "result": self.result_standardized,"score": [self.score["BLEU-4"],self.score["METEOR"]]}

