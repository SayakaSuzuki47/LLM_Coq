from module_py import split_SAU 
import os
from datasets import Dataset
from collections import deque
import pprint
import re

#選択問題のテキストファイルのみ格納されているフォルダ
input_dir_path='../data/test_select_pre_data/'
output_file_path="../data/data_json/test_select_text_data.json"

#選択問題のテキストファイルのパス一覧
files=[input_dir_path+f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))and f.endswith(".txt")]

texts=[]
for input_file_path in files:
    SAU_dct=split_SAU.split_for_SAU(input_file_path)
    for Assistant_num in range(len(SAU_dct["##Assistant"])):
        select_Assistant= SAU_dct["##Assistant"][Assistant_num]
        if '```' in select_Assistant:
            text_lst = [None]*(2+2*(Assistant_num-1))
            text_lst[0:2]=["##System\n",SAU_dct["##System"][0]]
            text_lst[2::2]=["##Assistant\n"]*Assistant_num
            text_lst[3::2] = [re.sub(r'```([^`]*)```\n', '', item)for item in SAU_dct["##Assistant"][0:Assistant_num]]
            text_lst.append("##User\n"+SAU_dct["##User"][Assistant_num])
            text_lst.append("##Assistant\n"+select_Assistant)
            texts.append({"text":"".join(text_lst)})
dataset=Dataset.from_list(texts)
dataset.to_json(output_file_path)   
print("Save"+output_file_path) 