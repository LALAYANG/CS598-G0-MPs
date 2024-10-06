###################################################################
# This is a list of all commands you need to run for MP3 on Colab.
###################################################################

# TODO: Clone your GitHub repository
! git clone [Your GitHub Link]
%cd [Your GitHub Repo]/MP3

# TODO: add your seed generated in MP1
seed = ""

# TODO: Replace the file path of selected_humaneval_[seed].jsonl generated in MP1
humaneval_input_dataset = "selected_humaneval_" + seed + ".jsonl"

# Set up requirements for dataset generation
! bash -x setup_dataset.sh

# Set up requirements for model prompting
! bash -x setup_models.sh

# Prompt the models, you can modify `MP3/task_1.py, MP3/task_2.py`
# The {input_dataset} is the JSON file consisting of 20 unique programs for your group that you generated in MP1 (selected_humaneval_[seed].jsonl)
! python3 task_2_dataset_generation.py {humaneval_input_dataset}

task_2_predict_json = "task_2_predict_" + seed + ".jsonl"
task_2_localize_json = "task_2_localize_" + seed + ".jsonl"
humanevalpack_input_dataset = "selected_humanevalpack_" + seed + ".jsonl"

! python3 task_2.py {humanevalpack_input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_predict_json} "False" |& tee task_2_predict.log
! python3 task_2.py {humanevalpack_input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_localize_json} "True" |& tee task_2_localize.log

%cd ..

# git push all nessacery files (e.g., *jsonl, *log) to your GitHub repository
