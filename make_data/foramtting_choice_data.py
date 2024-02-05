#library
import os

#input dir path
input_dir_path='../data/test_coq_lv_l/'
#output dir path
output_dir_path='../data/test_select_pre_data/'

#formatting 
def select_prompt_file(input_file_path,output_file_path):
    with open(input_file_path, 'r') as original, open(output_file_path, 'w') as modified:
        for line in original:
            modified.write(line)
            if "##Assistant" in line:
                modified.write("```Select the best tactic as the next instruction to be given to Coq from the following.\nThe choices are\n<TODO>\n")
                modified.write('Answer choice number is:```\n')

files=[f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))]
for file_name in files:
    input_file_path=input_dir_path+file_name
    output_file_path=output_dir_path+file_name
    select_prompt_file(input_file_path,output_file_path)  