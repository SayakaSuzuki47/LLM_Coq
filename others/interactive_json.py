from module_py import split_SAU 
import os
from datasets import Dataset
from collections import deque
import pprint
import re
import json

#各Coqファイルごとの対話形式のテキストファイルを入れたフォルダを指定する
input_dir_path='../data/coq_lv_l/'
output_file_path="../data/data_json/interactive_data.json"

files=[input_dir_path+f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))and f.endswith(".txt")]
texts=[]
for input_file_path in files:
    SAU_dct=split_SAU.split_for_SAU(input_file_path)
    Assis_len=len(SAU_dct["##Assistant"])
    for Assistant_num in range(Assis_len):
        select_Assistant= SAU_dct["##Assistant"][Assistant_num]
        if not(any( flag in select_Assistant for flag in ['+', '-', '*','Qed.'])):
            text_lst = [None]*(2+2*Assistant_num)
            text_lst[0:2]=["##System\n",SAU_dct["##System"][0]]
            text_lst[2::2]=["##Assistant\n"]*Assistant_num
            text_lst[3::2] = SAU_dct["##Assistant"][0:Assistant_num]
            text_lst.append("##User\n"+SAU_dct["##User"][Assistant_num])
            text_lst.append("##Assistant\n")
            ans_len=Assis_len-Assistant_num-1
            ans_con_text=[None]*(4*ans_len)
            ans_con_text[0::4]=["##User\n"]*(ans_len)
            ans_con_text[1::4]=SAU_dct["##User"][Assistant_num+1:]
            ans_con_text[2::4]=["##Assistant\n"]*(ans_len)
            ans_con_text[3::4] = SAU_dct["##Assistant"][Assistant_num+1:]
            
            #"text"には入力するテキスト
            #"ans_text"には続く正解のtactic
            #"ans_con_text"は"ans_text"のtactic以降を格納する
            texts.append({"text":"".join(text_lst),"ans_text":select_Assistant,"ans_con_text":"".join(ans_con_text),"inference_text":"","inference_ans":"","inference_con":"","score":""})
with open(output_file_path, 'w') as f:
    json.dump(texts, f)    