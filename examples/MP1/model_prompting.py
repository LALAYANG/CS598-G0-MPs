import os
import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def save_file(content, file_path):
  with open(file_path, 'w') as file:
    file.write(content)

def prompt_model(problem, model = "deepseek-ai/deepseek-coder-6.7b-base", quatization = True):
  # to download the model
  tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
  
  if quatization:
    # load with quatization
    model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=model,
            device_map='auto',
            torch_dtype=torch.bfloat16,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4'
            ),
        )
  else:
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path='deepseek-ai/deepseek-coder-6.7b-base',
            device_map='auto',
            torch_dtype=torch.bfloat16,
        )
        
  base_prompt = "Can you synthesize the following Python code?"
  prompt = f"{base_prompt}\n{problem}"
  inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
  outputs = model.generate(**inputs, max_length=1024)
  response = tokenizer.decode(outputs[0], skip_special_tokens=True)
  log = f"Prompt:\n{prompt}\nResponse:\n{response}"
  print(log)
  return log

def read_jsonl_and_return_prompts(file_path):
    prompts = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)            
            prompts.append(data)
    return prompts

if __name__ == "__main__":
    args = sys.argv[1:]
    dataset_jsonl = args[0]
    dataset = read_jsonl_and_return_prompts(dataset_jsonl)

    for data in dataset:
        print(data)
        exit(0)
    
    # response = prompt_model(problem)
    # save_file(response, file_path)
