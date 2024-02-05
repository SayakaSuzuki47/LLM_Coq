import json
import re
import pprint
import os
from module_py import file_processing
#input 
input_dir_path='../data/data_json/'

# #input file name
input_file_name=#生成した後のデータが保存されたjsonファイルの場所

def split_test(test_result):
    Q_num=len(test_result)
    for i in range(Q_num):
        result=test_result[i]
        inference_text=result['inference_text']
        flag=r"##System"
        splited_text=re.split(flag,inference_text)
        flag=r"##Assistant"
        splited_text=re.split(flag,splited_text[1])
        inference_ans=splited_text[1]
        inference_con=flag+flag.join(splited_text[2:])
        #新しく出力された部分の最初の##Assistantまでを生成されたtacticとする．
        result['inference_ans']=inference_ans
        #'inference_ans'以降の生成部分
        result['inference_con']=inference_con
    return(test_result,Q_num)

input_file_path=input_dir_path+file_path
with open(input_file_path) as f:
        test_result = json.load(f)
result=split_test(test_result)
with open(input_file_path, 'w') as f:
    json.dump(result[0], f)