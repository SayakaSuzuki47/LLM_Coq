import os
import json
import re
import pprint
import collections
from datasets import load_dataset 

#先頭に加えるprompt文を入力したテキストファイルを指定する．
input_prompt_file_name='cheat_sheet_goal_tactic.txt'
input_prompt_dir_path='../prompt/'
input_prompt_file_path=input_prompt_dir_path+input_prompt_file_name
with open(input_prompt_file_path) as f:
    prompt_text=f.read()

#datasetのダウンロード
input_data_file_name='interactive_format.json'
input_data_dir_path='../data/data_json/'
input_data_file_path=input_data_dir_path+input_data_file_name
dataset = load_dataset('json', data_files=input_data_file_path, split="train")

#promptに加工する関数
#"text"が加工されるテキスト文のindex
def prompt_format(example):
    #example["text"]がテキスト文なので適宜これを加工する関数に変える．
    example["text"]=f"{interactive_prompt}\n"+example["text"]
    return example
    
dataset = dataset.map(interactive_format)
output_file_path=input_data_dir_path+'cheat_sheet_interactive_format.json'
dataset.to_json(output_file_path)