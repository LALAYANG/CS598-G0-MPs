import sys
import random
import hashlib
from datasets import load_dataset

def generate_seed(netIDs):
    seed = int(hashlib.md5('_'.join(netIDs).encode()).hexdigest(), 16)
    return seed

def select_random_problems(netIDs, num_problems=20):
    seed = generate_seed(netIDs)
    random.seed(seed)
    print(f"NetIDs {netIDs} with seed {seed}")
    
    dataset = load_dataset("openai_humaneval")
    all_problems_output = "humaneval.jsonl"
    with open(all_problems_output, "w") as f:
        for item in dataset['test']:
            f.write(f"{item}\n")
    print(f"Entire Dataset saved to {all_problems_output}")

    problems = list(dataset['test'])
    selected_problems = random.sample(problems, num_problems)
    selected_problems_output = "selected_humaneval.jsonl"
    with open(selected_problems_output, "w") as f:
        for problem in selected_problems:
            f.write(f"{problem}\n")
    print(f"Selected {num_problems} problems saved to {selected_problems_output}")

if __name__ == "__main__":
    args = sys.argv[1:]
    select_random_problems(args)

