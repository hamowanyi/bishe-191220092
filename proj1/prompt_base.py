import re
import string
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
    def __init__(self,tokenizer_str='Salesforce/codet5-large',model_str='Salesforce/codet5-large',language='python',test=False,skipTokens=True):
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
        self.skip=skipTokens
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
        return re.split("[,:;*#'./\"\n(){}+-=_@!><&]", str)
    def get_first_char(self, str):
        for i in range(len(str)):
            if str[i] != ' ':
                if str[i] in string.ascii_uppercase:
                    return True, False
                elif str[i] in string.ascii_lowercase:
                    return False, True
        return False, False
    def judge_end(self, str, i):
        if i < len(str) - 1:
            if str[i + 1] in string.ascii_lowercase:
                return False
            else:
                return True
        else:
            return True
    def check_useful(self, str):
        text = ''':;*#'/\"\n(){}-!><&'''
        for c in text:
            if c in str:
                return False
        return True


    def ref_preprocess(self, ref):
        sList = ref.split('\n')
        res = ''
        if len(sList) > 1:
            i0 = 0
            while i0 < len(sList):
                if not self.check_useful(sList[i0]):
                    i0 = i0 + 1
                    continue
                if len(sList[i0]) == 0:
                    i0 = i0 + 1
                    continue
                is_upper, is_lower = self.get_first_char(sList[i0])
                if is_lower and not is_upper:
                    i1 = sList[i0].find('.')
                    if i1 != -1 and self.judge_end(sList[i0], i1):
                        res = res + sList[i0][:i1 + 1]
                        break
                    else:
                        res = res + sList[i0]
                    i0 = i0 + 1
                elif is_upper and not is_lower:
                    if len(res) > 0:
                        break
                    else:
                        i2 = sList[i0].find('.')
                        if i2 == -1:
                            res = res + sList[i0]
                        else:
                            if self.judge_end(sList[i0], i2):
                                res = res + sList[i0][:i2 + 1]
                                break
                        i0 = i0 + 1
                else:
                    i0 = i0 + 1
                    continue

        if len(res) == 0:
            return ref
        # clear blocks
        i2 = 0
        while i2 < len(res):
            if res[i2] != ' ':
                break
            else:
                i2 = i2 + 1
        res = res[i2:]
        return res


    def code_preprocess_python(self,code):
        sum_symbol = '''"""'''
        #sum with " " "
        pos = self.find_all(code, sum_symbol)
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


        sum_symbol = "'''"
        # sum with ' ' '
        pos = self.find_all(code, sum_symbol)
        if len(pos) > 1:
            replaceList = []
            i = 0
            # record begin_position of sum
            while i < len(pos) - 1:
                i1 = pos[i] - 1
                while i1 >= 0:
                    if code[i1] == ' ':
                        i1 = i1 - 1
                    else:
                        break
                if code[i1] == '\n':
                    replaceList.append([i1 + 1, pos[i + 1] + 2])
                    i = i + 2
                else:
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


        #sum with #
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
    def code_preprocess_java(self, code):
        sum_symbol = '/*'
        pos = self.find_all(code, sum_symbol)
        # maybe have sum:
        if len(pos) >= 1:
            replaceList = []
            i_head = 0
            while i_head < len(pos):
                i_tail = code.find('*/', pos[i_head] + 2)
                if i_tail != -1:
                    replaceList.append([pos[i_head], i_tail + 1])
                else:
                    break
                i_head = i_head + 1

            # record begin_position of sum
            i = len(replaceList) - 1
            # del sum
            while i >= 0:
                id = replaceList[i]
                if (id[1] < len(code) - 1):
                    code = code[:id[0]] + code[id[1] + 1:]
                else:
                    code = code[:id[0]]
                i -= 1

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
                i2 = i1 + 1
                while i2 < len(code):
                    if code[i2] != '\n':
                        i2 = i2 + 1
                    else:
                        break
                replaceList.append([i1 + 1, i2 - 1])
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

        # del blocks
        pos = self.find_all(code, '\n')
        replaceList = []
        i = 0
        for i in range(len(pos) - 1):
            if self.all_block(code[pos[i]:pos[i + 1]]):
                replaceList.append(pos[i + 1])
        i = len(replaceList) - 1
        while i >= 0:
            code = code[:replaceList[i]] + code[replaceList[i] + 1:]
            i = i - 1

        return code
    def code_preprocess_js(self, code):
        return self.code_preprocess_java(code)
    def code_preprocess_go(self, code):
        return self.code_preprocess_java(code)
    def code_preprocess_php(self, code):
        sum_symbol = '/*'
        pos = self.find_all(code, sum_symbol)
        # maybe have sum:
        if len(pos) >= 1:
            replaceList = []
            i_head = 0
            while i_head < len(pos):
                i_tail = code.find('*/', pos[i_head] + 2)
                if i_tail != -1:
                    replaceList.append([pos[i_head], i_tail + 1])
                else:
                    break
                i_head = i_head + 1

            # record begin_position of sum
            i = len(replaceList) - 1
            # del sum
            while i >= 0:
                id = replaceList[i]
                if (id[1] < len(code) - 1):
                    code = code[:id[0]] + code[id[1] + 1:]
                else:
                    code = code[:id[0]]
                i -= 1

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
                i2 = i1 + 1
                while i2 < len(code):
                    if code[i2] != '\n':
                        i2 = i2 + 1
                    else:
                        break
                replaceList.append([i1 + 1, i2 - 1])
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

        pos = self.find_all(code, '#')
        # maybe have #:
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
                i2 = i1 + 1
                while i2 < len(code):
                    if code[i2] != '\n':
                        i2 = i2 + 1
                    else:
                        break
                replaceList.append([i1 + 1, i2 - 1])
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

        # del blocks
        pos = self.find_all(code, '\n')
        replaceList = []
        i = 0
        for i in range(len(pos) - 1):
            if self.all_block(code[pos[i]:pos[i + 1]]):
                replaceList.append(pos[i + 1])
        i = len(replaceList) - 1
        while i >= 0:
            code = code[:replaceList[i]] + code[replaceList[i] + 1:]
            i = i - 1

        return code
    def code_preprocess_ruby(self, code):
        sum_symbol = '=begin'
        pos = self.find_all(code, sum_symbol)
        # maybe have sum:
        if len(pos) >= 1:
            replaceList = []
            i_head = 0
            while i_head < len(pos):
                i_tail = code.find('=end', pos[i_head] + 2)
                if i_tail != -1:
                    replaceList.append([pos[i_head], i_tail + 1])
                else:
                    break
                i_head = i_head + 1

            # record begin_position of sum
            i = len(replaceList) - 1
            # del sum
            while i >= 0:
                id = replaceList[i]
                if (id[1] < len(code) - 1):
                    code = code[:id[0]] + code[id[1] + 1:]
                else:
                    code = code[:id[0]]
                i -= 1


        pos = self.find_all(code, '#')
        # maybe have #:
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
                i2 = i1 + 1
                while i2 < len(code):
                    if code[i2] != '\n':
                        i2 = i2 + 1
                    else:
                        break
                replaceList.append([i1 + 1, i2 - 1])
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

        # del blocks
        pos = self.find_all(code, '\n')
        replaceList = []
        i = 0
        for i in range(len(pos) - 1):
            if self.all_block(code[pos[i]:pos[i + 1]]):
                replaceList.append(pos[i + 1])
        i = len(replaceList) - 1
        while i >= 0:
            code = code[:replaceList[i]] + code[replaceList[i] + 1:]
            i = i - 1

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
    def set_prompt_java(self,code,type=1):
        if type==0:
            code = code + '''\n\n/*is used to'''
        elif type==1:
            replaceID=code.find('{\n')
            if replaceID==-1:
                code='''/*is used to<extra_id_0>\n'''+code
            elif replaceID<len(code):
                replaceID = replaceID + 2
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
                    code = code[:replaceID] + '''/*is used to<extra_id_0>\n''' + blocks + code[replaceID:]
                else:
                    code='''/*is used to<extra_id_0>\n'''+code
        elif type==3:
            code='''/*is used to<extra_id_0>\n'''+code
        code = code.replace('\n', '\r\n')
        return code
    def set_prompt_js(self,code,type=1):
        return self.set_prompt_java(code,type)
    def set_prompt_go(self,code,type=1):
        return self.set_prompt_java(code,type)
    def set_prompt_php(self,code,type=1):
        return self.set_prompt_java(code,type)
    def set_prompt_ruby(self,code,type=1):
        return self.set_prompt_java(code,type)

    def denoise(self,result):
        if self.skip:
            sList = self.string_split(result)
            result = max(sList, key=len, default='')
        else:
            sList=result.split('<extra_id_')
            for i in range(len(sList)):
                cut=sList[i].find('>')
                if cut==-1:
                    continue
                else:
                    str=sList[i][cut+1:]
                    strList=self.string_split(str)
                    str=max(strList, key=len, default='')
                    sList[i]=str
            result=max(sList,key=len,default='')


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
        if self.input_size>512:
            self.result='Code too long,keep in 512.'
            return
        if torch.cuda.is_available():
            input_ids=input_ids.cuda()
        generated_ids = self.model.generate(input_ids, max_length=25)
        self.result=self.tokenizer.decode(generated_ids[0],skip_special_tokens=self.skip)
    def run(self,input):
        self.text=input[0]
        self.reference.clear()
        preprocess_ref = self.ref_preprocess(input[1])
        if self.language=='java' and preprocess_ref.find('@')!=-1:
            preprocess_ref=preprocess_ref[:preprocess_ref.find('@')]
            if len(preprocess_ref)==0:
                preprocess_ref=input[1]
        elif self.language=='js' and preprocess_ref.find('@')!=-1:
            preprocess_ref=preprocess_ref[:preprocess_ref.find('@')]
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
                self.text = self.set_prompt_java(self.text,type=3)
            elif self.language=='js':
                self.text = self.code_preprocess_js(self.text)
                self.text = self.set_prompt_js(self.text, type=3)
            elif self.language=='go':
                self.text = self.code_preprocess_go(self.text)
                self.text = self.set_prompt_go(self.text, type=3)
            elif self.language=='php':
                self.text = self.code_preprocess_php(self.text)
                self.text = self.set_prompt_php(self.text, type=3)
            elif self.language=='ruby':
                self.text = self.code_preprocess_ruby(self.text)
                self.text = self.set_prompt_ruby(self.text, type=3)
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
        return {"code": self.text, "code-length":self.input_size,"reference": self.reference[0], "result": self.result_standardized,"score": [self.score["BLEU-4"],self.score["METEOR"]]}

