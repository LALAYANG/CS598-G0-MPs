import jsonlines
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import re
from datasets import load_dataset

#####################################################
# Please finish all TODOs in this file for MP3;
#####################################################

def prompt_model(dataset, model_name = "deepseek-ai/deepseek-coder-6.7b-instruct", localize = False):
    print(f"Working with {model_name} prompt type {localize}...")
    
    # TODO: download the model
    # TODO: load the model with quantization

    results = []
    for entry in dataset:
        if localize:
            # TODO: create prompt for the model
            # Tip : Use can use any data from the dataset to create 
            #       the prompt
            prompt = ""
    
            # TODO: prompt the model and get the response
            response = ""

            print(f"Task_ID {entry['task_id']}:\nprompt:\n{prompt}\nresponse:\n{response}")
            # Add the result to the list
            results.append({
                "task_id": entry["task_id"],
                "prompt": prompt,
                "response": response,
            })
        
        else:
            # TODO: create prompt for the model
            # Tip : Use can use any data from the dataset to create 
            #       the prompt
            prompt = ""
    
            # TODO: prompt the model and get the response
            response = ""

            # TODO: process the response and save it to results
            parsed_output = ""

            verdict = False
    
            print(f"Task_ID {entry['task_id']}:\nprompt:\n{prompt}\nresponse:\n{response}\nis_expected:\n{verdict}")
            # Add the result to the list
            results.append({
                "task_id": entry["task_id"],
                "prompt": prompt,
                "response": response,
                "is_expected": verdict
            })
        
    return results

def read_jsonl(file_path):
    dataset = []
    with jsonlines.open(file_path) as reader:
        for line in reader: 
            dataset.append(line)
    return dataset

def write_jsonl(results, file_path):
    with jsonlines.open(file_path, "w") as f:
        for item in results:
            f.write_all([item])

if __name__ == "__main__":
    """
    This Python script is to run prompt LLMs for code synthesis.
    Usage:
    `python3 Task_[ID].py <input_dataset> <model> <output_file> <if_localize>`|& tee prompt.log

    Inputs:
    - <input_dataset>: A `.jsonl` file, which should be your team's dataset containing 20 HumanEval problems.
    - <model>: Specify the model to use. Options are "deepseek-ai/deepseek-coder-6.7b-base" or "deepseek-ai/deepseek-coder-6.7b-instruct".
    - <output_file>: A `.jsonl` file where the results will be saved.
    - <if_localize>: Set to 'True' or 'False' to enable localize prompt
    
    Outputs:
    - You can check <output_file> for detailed information.
    """
    args = sys.argv[1:]
    input_dataset = args[0]
    model = args[1]
    output_file = args[2]
    if_localize = args[3] # True or False
    
    if not input_dataset.endswith(".jsonl"):
        raise ValueError(f"{input_dataset} should be a `.jsonl` file!")
    
    if not output_file.endswith(".jsonl"):
        raise ValueError(f"{output_file} should be a `.jsonl` file!")
    
    localize = True if if_localize == "True" else False
    
    dataset = read_jsonl(input_dataset)
    results = prompt_model(dataset, model, localize)
    write_jsonl(results, output_file)