from transformers import AutoTokenizer, T5ForConditionalGeneration
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large")

text='''public function editRoles(User $user, $model)
    {
        /*is used to<extra_id_0>*/
        $another = $user->id != $model->id;
        return $another && $user->hasPermission('edit_users');
    }'''
#Returns a dictionary from a URL params
text=text.replace('\n','\r\n')
print(text+'\n\n')
input_ids = tokenizer(text, return_tensors="pt").input_ids

# simply generate a single sequence
generated_ids = model.generate(input_ids, max_length=25)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=False))
