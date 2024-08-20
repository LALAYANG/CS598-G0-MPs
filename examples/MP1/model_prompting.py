import os
import sys
import jsonlines
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def save_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

def prompt_model(dataset, model_name = "deepseek-ai/deepseek-coder-6.7b-base", quatization = True):
    print(f"Working with {model_name} quatization {quatization}...")
    
    # download the model
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
  
    if quatization:
        # loading with quatization
        model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
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
        # loading without quatization
        model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
                device_map='auto',
                torch_dtype=torch.bfloat16
                )

    base_prompt = "Can you synthesize the following Python code?"
    results = {}
    for case in dataset:
        prompt = f"{base_prompt}\n{case['prompt']}"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_length=1024)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Task_ID {case['task_id']}:\nPrompt:\n{prompt}\nResponse:\n{response}")
        if case["task_id"] not in results:
            results[case["task_id"]] = case.copy()
        results[case["task_id"]].update({"response": response})
    return results

def read_jsonl(file_path):
    dataset = []
    with jsonlines.open(file_path) as reader:
        for line in reader: 
            dataset.append(line)
    return dataset

def write_jsonl(dicts, file_path):
    with jsonlines.open(file_path, "w") as f:
        for item in dicts:
            f.write_all([item])

if __name__ == "__main__":
    args = sys.argv[1:]
    dataset_jsonl = args[0]
    model = args[1]
    file_path = args[2]
    if_quatization = args[3] # True or False
    
    if not file_path.endswith(".jsonl"):
        raise ValueError(f"{file_path} should be a `.jsonl` file!")
    
    quatization = True if if_quatization == "True" else False
    
    dataset = read_jsonl(dataset_jsonl)
    results = prompt_model(dataset, model, quatization)
    write_jsonl(results, file_path)
