import os
from collections import deque
import pprint
import re
import json
import ast
import pprint

#input file path
input_dir_path='../data/data_json/'
input_file_name='AAA.json'

#output dir path
output_dir_path='../data/data_json/'
output_file_name='BBB.json'
output_file_path=output_dir_path+output_file_name

def split_text_Num(text):
    # 数字で文字列を分割
    pattern = r':\s*(\d+)\s*```'
    matches = re.split(pattern, text)
    # 分割されたリストから空の要素を削除
    result = [match.strip() for match in matches if match.strip() != '']
    return result

input_file_path=input_dir_path+input_file_name

select_data_lst=[]
with open(input_file_path) as f:
    for line in f:
        text_dct=json.loads(line)
        split_lst=split_text_Num(text_dct["text"])
        reault_dct={"text":repr(split_lst[0]+":"),"ans_num":split_lst[1],"ans_text":repr(split_lst[2]),"inference_num":"","inference_text":""}
        select_data_lst.append(reault_dct)

with open(output_file_path, 'w') as f:
    json.dump(select_data_lst, f)