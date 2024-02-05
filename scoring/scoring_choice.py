import json
import re
import pprint
from module_py import file_processing

#input 
input_dir_path='../data/data_json/'
input_file_name='AAA.json'

def score_select_test(test_result):
    Q_num=len(test_result)
    max_score=Q_num
    score=0
    mis_gen=0
    mis_gen_lst=[]
    mis_lst=[]
    for i in range(Q_num):
        result=test_result[i]
        text=result["inference_text"]
        pattern = r'Answer choice number is:'
        splited_text = re.split(pattern, text)
        pattern=r'(?:\d+)?\s*goal'
        splited_text = re.split(pattern, splited_text[1])
        num_splited=re.split(r'(\d+)', "".join(splited_text[0]))
        inference_ans=''
        #選択した数字を生成したかどうか判定する
        if len(num_splited)<2:
            test_result[i]["inference_num"]="0"
            mis_gen+=1
            mis_gen_lst.append(i)
        else:
            test_result[i]["inference_num"]=num_splited[1]
            inference_ans="".join(num_splited[2:])
            if result["ans_num"]==num_splited[1]:
                score+=1
            else:
                mis_lst.append(i)
        #選択した数字を入力する
        test_result[i]['inference_ans']=inference_ans
    return(test_result,max_score,score,mis_gen,mis_gen_lst,mis_lst)

input_file_path=input_dir_path+input_file_name
with open(input_file_path) as f:
    test_result = json.load(f)
    
result=score_select_test(test_result)
#選択した数字等を格納する
with open(input_file_path, 'w') as f:
    json.dump(result[0], f)

print(input_file_name)
print("Question number is : "+ str(result[1]))
print("score : "+str(result[2]))
print("Not generate  : "+str(result[3]))
print(result[4])
print("Miss")
print(result[5]) 