from transformers import AutoTokenizer, T5ForConditionalGeneration
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large")

text='''/*is used to<extra_id_0>
protected final void fastPathOrderedEmit(U value, boolean delayError, Disposable disposable) {
        final Observer<? super V> observer = downstream;
        final SimplePlainQueue<U> q = queue;
        if (wip.get() == 0 && wip.compareAndSet(0, 1)) {
            if (q.isEmpty()) {
                accept(observer, value);
                if (leave(-1) == 0) {
                    return;
                }
            } else {
                q.offer(value);
            }
        } else {
            q.offer(value);
            if (!enter()) {
                return;
            }
        }
        QueueDrainHelper.drainLoop(q, observer, delayError, disposable, this);
    }'''
#Returns a dictionary from a URL params
text=text.replace('\n','\r\n')
print(text+'\n\n')
input_ids = tokenizer(text, return_tensors="pt").input_ids

# simply generate a single sequence
generated_ids = model.generate(input_ids, max_length=25)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=False))
