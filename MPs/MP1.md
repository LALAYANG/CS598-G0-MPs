## Prepare your dataset
[HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) includes 164 Python problems for LLM evaluation. Each team should automatically generate a unique dataset of 20 problems. To generate your dataset, please follow the steps below:

1. Run [setup.sh](../examples/MP1/setup.sh) by command `bash -x setup.sh` to install required Python libraries to use huggingface APIs.

2. Run [datset_generation.py](../examples/MP1/dataset_generation.py) by the following command to generate a dataset including 20 problems for your team. You should run with the netIDs of all your team members:
```
python3 dataset_generation.py <netID1> <netID2> <netID3> |& tee dataset_generation.log
```

You will get the following outputs (also saved in `dataset_generation.log`):
```
NetIDs ['ID1', 'ID2', 'ID3'] with seed 263643969642646976669746046825268733062
Entire Dataset saved to humaneval.jsonl
Selected 20 problems saved to selected_humaneval_263643969642646976669746046825268733062.jsonl
```
where:
a seed generated (263643969642646976669746046825268733062 in this example) is binded to your netIDs, 
you will get `humaneval.jsonl` with entire HumanEval dataset
and `selected_humaneval_[seed].jsonl` with 20 problems that you need in the following tasks.

3. Upload the following files to your Github Repository (under folder MP1):
- `selected_humaneval_[seed].jsonl`
- `humaneval.jsonl`
- `dataset_generation.log`

4. Remember to update your `seed` in your MP1 report.