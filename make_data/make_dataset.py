import os
import pprint
from datasets import load_dataset,load_from_disk

def make_dataset_from_files(input_dir_path,output_file_path):
    files=[input_dir_path+f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))and f.endswith(".txt")]
    dataset = load_dataset('text', data_files=files, split="train",sample_by= "document")
    dataset.to_json(output_file_path)   
    print("Save"+output_file_path)

#data dir path
output_dir_path='../data/data_json/'

#各スクリプトごとのデータが入ったフォルダ
input_dir_path='../data/test_coq_lv_l/'
file_name='test_interactive_format.json'
output_file_path=output_dir_path+file_name
files=[input_dir_path+f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))and f.endswith(".txt")]
dataset = load_dataset('text', data_files=files, split="train",sample_by= "document")
dataset.to_json(output_file_path)