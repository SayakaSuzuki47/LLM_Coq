# ### パラメータ
#model_name
model_name="meta-llama/Llama-2-7b-hf"

#flow 学習させる datasetの順番
flow="simple_select"

#モデルのloadの仕方
load_in = "fp32" # "fp32", "fp16", "int8" のいずれかを設定してください
set_num=32
prompt=''
SFT_model_dir="./output/LoRA/"+exp+prompt+model_name.replace('/', '_')+"/"+flow+"/"
SFT_model_name=flow+"/"+model_name
SFT_model_name=SFT_model_name.replace('/', '_')

# ### work
import os
os.chdir('./work')
# ## Install
#!pip install wandb --upgrade
from transformers.trainer_utils import set_seed
# 乱数シードを42に固定
set_seed(42)
import time
from pprint import pprint
from datasets import load_dataset

# ### load model 
#load base model
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoTokenizer,AutoModelForSequenceClassification,LlamaTokenizer, AutoModelForCausalLM,AutoModelForSeq2SeqLM

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

cache_dir = "./model_cache"    # モデルのキャッシュを保存するフォルダ
model_kwargs = {"trust_remote_code": True, "device_map": "auto", "low_cpu_mem_usage": True, "cache_dir": cache_dir}


if load_in == "fp16":
    model_kwargs["variant"] = "fp16"
    model_kwargs["torch_dtype"] = torch.float16
elif load_in == "int8":
    model_kwargs["variant"] = "int8"
    model_kwargs["load_in_8bit"] = True

tokenizer = AutoTokenizer.from_pretrained(model_name, additional_special_tokens=['▁▁'])
#学習済みモデルのダウンロード
model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)

tokenizer.pad_token = tokenizer.eos_token
# Fix weird overflow issue with fp16 training
tokenizer.padding_side = "right"

import peft
import psutil
from pprint import pprint
from datasets import load_dataset
from transformers import TrainingArguments, DataCollatorForLanguageModeling, Trainer
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

from importlib import import_module
params=import_module("param.LoRA."+SFT_model_name)
peft_config = peft.LoraConfig(
    r=params.lora_r,
    lora_alpha=params.lora_alpha,
    lora_dropout=params.lora_dropout,
    bias=params.bias,
    task_type=params.task_type,
    target_modules=params.target_modules
)
model = peft.get_peft_model(model, peft_config)
from transformers import TrainingArguments, DataCollatorForLanguageModeling, Trainer
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
#学習済みモデルの構築
SFT_model = PeftModel.from_pretrained(model, lora_model_dir)
SFT_model = peft.get_peft_model(SFT_model, peft_config)

#生成
import json

#text:LLMに入力したいテキスト
#gene_Num：入力テキストの続きに出力したいテキストのトークン数を指定する．入力のテキストトークン数+gene_Numで計算する
def generate_text(text,gene_Num):
    start_time = time.time()
    inputs = tokenizer(
    text, 
    return_tensors="pt"
    )
    max_length=len(inputs['input_ids'][0])+gene_Num
    time_start = time.time()
    outputs = model.generate(
        **inputs,
        pad_token_id=tokenizer.eos_token_id,
        max_length=max_length,
        repetition_penalty =1.1
        )
    decode_output=repr(tokenizer.decode(outputs.tolist()[0], skip_special_tokens=True))
    text_len=len(text)
    result_text=decode_output

    end_time = int(time.time() - start_time)
    # convert second to hour, minute and seconds
    hour = end_time // 3600
    minute = (end_time % 3600) // 60
    second = (end_time % 3600 % 60)
    time_str=str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    print(time_str)
    return (result_text,end_time)

#生成に使用するデータの形はdict型{"text": }のリスト(テキストの個数分の大きさ)にする．
test_data_path=#生成に使用するデータへのパス
with open(test_data_path) as f:
    test_dct_lst = json.load(f)

gen_time=0
i=0
for dct in test_dct_lst:
    text=dct["text"]
    result=generate_text(text,gene_Num)
    #dictの"inference_text"に生成した文字列を格納する．
    dct["inference_text"]=result[0]
    gen_time=gen_time+result[1]
    mean_time=gen_time/len(test_dct_lst)
     # convert second to hour, minute and seconds
    hour = mean_time // 3600
    minute = (mean_time % 3600) // 60
    second = (mean_time % 3600 % 60)
    time_str=str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    i=i+1
    print(i)
print("mean generate time: "+time_str) 

#元のファイルを上書きする
test_file_name=test_data_path.split('.')[1]
test_file_name=test_file_name.split('/')[2]
result_path=SFT_model_dir+test_file_name+'_'+SFT_model_name+"FF.json"
with open(result_path, 'w') as f:
    json.dump(test_dct_lst, f)

#生成するのにかかった時間の平均を保存する．
result_time_path=SFT_model_dir+test_file_name+'_'+SFT_model_name+'_'+"time_data.txt"
with open(result_time_path, 'w') as f:
    f.write("Test:Inference  "+"mean generate time: "+time_str+"\n")

# メモリやGPUの開放
del test_dct_lst
del model
del tokenizer
import torch
torch.cuda.empty_cache()