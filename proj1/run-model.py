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
text='''def is_event_loop_running_qt4(app=None):
    if app is None:
        app = get_app_qt4([''])
    if hasattr(app, '_in_event_loop'):
        return app._in_event_loop
    else:
        return False

""" is used to'''

inputs = tokenizer(text, return_tensors="pt").input_ids
outputs = model.generate(inputs,max_length=len(inputs[0])+25)
print(tokenizer.decode(outputs[0], skip_special_tokens=False))



