import jsonlines
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import re
from datasets import load_dataset

#####################################################
# Please finish all TODOs in this file for MP3;
#####################################################

def prompt_model(dataset, model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"):
    print(f"Working with {model_name} prompt type {localize}...")
    
    # TODO: download the model
    # TODO: load the model with quantization

    results = []
    for entry in dataset:
      # TODO: prompt the model and get the response, you can create any helper functions to help you.
      original_prompt = ""
      original_response = ""
      print(f"Task_ID {entry['task_id']}:\noriginal_prompt:\n{original_prompt}\noriginal_response:\n{original_response}")
      dataflow_change_prompt = ""
      dataflow_change_response = ""
      print(f"Task_ID {entry['task_id']}:\noriginal_prompt:\n{original_prompt}\noriginal_response:\n{original_response}")
      controlflow_change_prompt = ""
      controlflow_change_response = ""
      print(f"Task_ID {entry['task_id']}:\noriginal_prompt:\n{original_prompt}\noriginal_response:\n{original_response}")

      #TODO: Parse results
      original_result = ""
      dataflow_change_result = ""
      controlflow_change_result = ""
      
      # TODO: Add the result to the list
      results.append({
        "task_id": entry["task_id"],
        "original_prompt": original_prompt,
        "original_response": original_response,
        "dataflow_change_prompt": dataflow_change_prompt,
        "dataflow_change_response": dataflow_change_response,
        "controlflow_change_prompt" : controlflow_change_prompt,
        "controlflow_change_response" : controlflow_change_response
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
    `python3 task_1.py <input_dataset> <model> <output_file> <if_localize>`|& tee prompt.log

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
    
    if not input_dataset.endswith(".jsonl"):
        raise ValueError(f"{input_dataset} should be a `.jsonl` file!")
    
    if not output_file.endswith(".jsonl"):
        raise ValueError(f"{output_file} should be a `.jsonl` file!")
    
    dataset = read_jsonl(input_dataset)
    results = prompt_model(dataset, model, localize)
    write_jsonl(results, output_file)
