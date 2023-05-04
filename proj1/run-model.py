"""from transformers import AutoTokenizer, T5ForConditionalGeneration
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large")

text=''''''
#Returns a dictionary from a URL params
text=text.replace('\n','\r\n')
print(text+'\n\n')
input_ids = tokenizer(text, return_tensors="pt").input_ids

# simply generate a single sequence
generated_ids = model.generate(input_ids, max_length=25)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=False))"""

from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("codeparrot/codeparrot")
model = AutoModelWithLMHead.from_pretrained("codeparrot/codeparrot")
text='''def get_video_url_from_video_id(video_id):
    data = [""] * 256
    for index, _ in enumerate(data):
        t = index
        for i in range(8):
            t = -306674912 ^ unsigned_right_shitf(t, 1) if 1 & t else unsigned_right_shitf(t, 1)
        data[index] = t

    def tmp():
        rand_num = random.random()
        path = "/video/urls/v/1/toutiao/mp4/{video_id}?r={random_num}".format(video_id=video_id,
                                                                              random_num=str(rand_num)[2:])
        e = o = r = -1
        i, a = 0, len(path)
        while i < a:
            e = ord(path[i])
            i += 1
            if e < 128:
                r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ e)]
            else:
                if e < 2048:
                    r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (192 | e >> 6 & 31))]
                    r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | 63 & e))]
                else:
                    if 55296 <= e < 57344:
                        e = (1023 & e) + 64
                        i += 1
                        o = 1023 & t.url(i)
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (240 | e >> 8 & 7))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | e >> 2 & 63))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | o >> 6 & 15 | (3 & e) << 4))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | 63 & o))]
                    else:
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (224 | e >> 12 & 15))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | e >> 6 & 63))]
                        r = unsigned_right_shitf(r, 8) ^ data[255 & (r ^ (128 | 63 & e))]

        return "https://ib.365yg.com{path}&s={param}".format(path=path, param=unsigned_right_shitf(r ^ -1, 0))

    while 1:
        url = tmp()
        if url.split("=")[-1][0] != "-":  # 参数s不能为负数
            return url

""" This function'''

inputs = tokenizer(text, return_tensors="pt").input_ids
outputs = model.generate(inputs,max_length=len(inputs[0])+25)
print(tokenizer.decode(outputs[0], skip_special_tokens=False))



