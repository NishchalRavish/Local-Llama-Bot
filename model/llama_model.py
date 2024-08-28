import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

class LlamaQA:
    def __init__(self, model_name='meta-llama/Llama-2-70b'):
        self.tokenizer = LlamaTokenizer.from_pretrained(model_name)
        self.model = LlamaForCausalLM.from_pretrained(model_name)
    
    def get_answer(self, question):
        inputs = self.tokenizer.encode(question, return_tensors='pt').to('cpu')
        outputs = self.model.generate(inputs, max_length=500,num_return_sequences=1)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return answer