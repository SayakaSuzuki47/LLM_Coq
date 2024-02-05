#From the results of executing coqtop -lv and coqtop -l
#Process the response format of #System & #User & #Assistant.

#import library
import os
import pprint

#input dir path
#Directory containing the result of executing coqtop -lv
input_dir_path='../data/coq_lv/'
#Directory containing the result of executing coqtop -l
input_dir_path_l='../data/coq_l/'

#output dir path
output_dir_path='../data/coq_lv_l/'

files=[f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))]

#process_lv_l
#From the results of executing coqtop -lv and coqtop -l
#Process the response format of #System & #User & #Assistant.
def process_lv_l(lv_first,lv_lst,l_first,l_lst,text_lst,texts,flag):
    if (len(l_lst)==0)and(lv_first==l_first):
        if flag:
            text_lst.append(texts+lv_first)
            text_lst.append('##Assistant'+'\n'+ ''.join(lv_lst))
        else:
            text_lst.append(texts)
            text_lst.append(lv_first)
            text_lst.append('##Assistant'+'\n'+ ''.join(lv_lst))
        return(text_lst) 
    elif "Show." in lv_first:
        lv_first=lv_first.replace('Show.','##User')
        text_lst.append(texts)
        text_lst.append(lv_first)
        texts=''
        lv_first,lv_lst=lv_lst[0],lv_lst[1:]
        return process_lv_l(lv_first,lv_lst,l_first,l_lst,text_lst,texts,flag)
    elif lv_first==l_first:
        if flag:
            texts=texts+lv_first
        else:
            text_lst.append(texts)
            texts=lv_first
            flag=True
        lv_first,lv_lst=lv_lst[0],lv_lst[1:]
        l_first,l_lst=l_lst[0],l_lst[1:]
        return process_lv_l(lv_first,lv_lst,l_first,l_lst,text_lst,texts,flag)
    elif lv_first!=l_first:
        if flag:
            text_lst.append(texts)
            texts='##Assistant'+'\n'+lv_first
            flag=False
        else:
            texts=texts+lv_first
        lv_first,lv_lst=lv_lst[0],lv_lst[1:]
        return process_lv_l(lv_first,lv_lst,l_first,l_lst,text_lst,texts,flag)
    else:
        raise ValueError("An exception occurred")

for file_name in files:
    #Def file path
    input_file_path=input_dir_path+file_name
    input_file_path_l=input_dir_path_l+file_name
    output_file_path=output_dir_path+file_name

    #open file
    with open(input_file_path, 'r') as f:
        lv_lst=f.readlines()
    with open(input_file_path_l, 'r') as f:
        l_lst=f.readlines()
    text_lst = ['##System'+'\n']

    #process
    texts=''
    flag=False  
    lv_first,lv_lst=lv_lst[0],lv_lst[1:]
    l_first,l_lst=l_lst[0],l_lst[1:]
    result=process_lv_l(lv_first,lv_lst,l_first,l_lst,text_lst,texts,flag)

    #save file
    with open(output_file_path, 'w') as f:
        for i in result:
            f.write(i)