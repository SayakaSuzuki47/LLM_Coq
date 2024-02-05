# ### パラメータ
#model_name
model_name="meta-llama/Llama-2-7b-hf"

#flow 学習させる datasetを管理
#simpleは対話形式,"select"は選択問題形式を表している．
flow="simple"
#flow="simple_select"

#モデルのloadの仕方
load_in = "fp32" # "fp32", "fp16", "int8" のいずれか
set_num=32

# 変数名等
flow_lst=flow.split("_")

#各datasetのファイルの場所を書く
def dataset_name(str_name):
    if str_name == "simple" :
        data_file_name="./data/interactive_format.json"
    elif str_name == "select" :
        data_file_name="./data/select_learn_data_plus_Assis.json"
    else:
        print("have not data")
        data_file_name=""
    return data_file_name

def select_dataset(i,lst):
    i_name=lst[i]
    if not( "and" in i_name ):
        return(dataset_name(i_name))
    else:
        names=i_name.split("and")
        name_lst=[ dataset_name(name) for name in names]
        return name_lst

#実験番号
exp="exp_2/"
#プロンプト
prompt=''

#modelの保存等に関する情報
SFT_model_dir="./output/Fine_Tuning/"+exp+prompt+model_name.replace('/', '_')+"/"+flow+"/"
SFT_model_name=flow+"/"+model_name
SFT_model_name=SFT_model_name.replace('/', '_')
print(SFT_model_dir)
print(SFT_model_name)

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

# ## Wandb
#学習状況を可視化
import wandb
import os
wandb.login()
run=wandb.init(project=('Exp_2_Full-FF_'+prompt.replace('/', '_')+SFT_model_name))

#loggingを設定
from transformers import logging
logging.set_verbosity(logging.CRITICAL)

# ### load model 
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,AutoTokenizer,AutoModelForSequenceClassification,LlamaTokenizer,AutoModelForCausalLM,AutoModelForSeq2SeqLM

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

 # モデルのキャッシュを保存するフォルダ
cache_dir = "./model_cache"   
model_kwargs = {"trust_remote_code": True, "device_map": "auto", "low_cpu_mem_usage": True, "cache_dir": cache_dir}

if load_in == "fp16":
    model_kwargs["variant"] = "fp16"
    model_kwargs["torch_dtype"] = torch.float16
elif load_in == "int8":
    model_kwargs["variant"] = "int8"
    model_kwargs["load_in_8bit"] = True

tokenizer = AutoTokenizer.from_pretrained(model_name, additional_special_tokens=['▁▁'])
model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)

tokenizer.pad_token = tokenizer.eos_token
# Fix weird overflow issue with fp16 training
tokenizer.padding_side = "right" 
import peft
from importlib import import_module
import psutil
from pprint import pprint
from datasets import load_dataset
from transformers import TrainingArguments, DataCollatorForLanguageModeling, Trainer
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

# # 学習1回目
# dataset
i=0
data_files=select_dataset(i,flow_lst)
print(data_files)
dataset = load_dataset('json', data_files=data_files, split="train")
dataset =dataset.shuffle(seed=42)
max_seq_length = max([len(tokenizer.tokenize(text)) for text in dataset["text"] ])
min_seq_length = min([len(tokenizer.tokenize(text)) for text in dataset["text"] ])

### Leaning Parameter
#学習に関するパラメータはそれぞれ別のファイルに書き込み，呼び出す．
param_file_name=flow_lst[i]+'_'+model_name.replace('/', '_')
params=import_module(f'work.param.LoRA.{param_file_name}')
print(param_file_name)

### LoRA
# Set training parameters
peft_config = peft.LoraConfig(
    r=params.lora_r,
    lora_alpha=params.lora_alpha,
    lora_dropout=params.lora_dropout,
    bias=params.bias,
    task_type=params.task_type,
    target_modules=params.target_modules
)
model = peft.get_peft_model(model, peft_config)

training_arguments = TrainingArguments(
    output_dir=SFT_model_dir,
    num_train_epochs=params.num_train_epochs,
    per_device_train_batch_size=params.per_device_train_batch_size,
    gradient_accumulation_steps=params.gradient_accumulation_steps,
    optim=params.optim,
    save_steps=params.save_steps,
    logging_steps=params.logging_steps,
    learning_rate=params.learning_rate,
    weight_decay=params.weight_decay,
    fp16=params.fp16,
    bf16=params.bf16,
    max_grad_norm=params.max_grad_norm,
    max_steps=params.max_steps,
    warmup_ratio=params.warmup_ratio,
    group_by_length=params.group_by_length,
    lr_scheduler_type=params.lr_scheduler_type,
    report_to=params.report_to
)
data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

# 学習の実行
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    dataset_text_field=params.dataset_text_field,
    max_seq_length=params.max_seq_length,
    formatting_func=params.formatting_func,
    data_collator=params.data_collator,
    tokenizer=tokenizer,
    args=training_arguments,
    packing=params.packing,
)
model.config.use_cache = False

print('start')
time_start = time.time()
model.config.use_cache = False
trainer.train()
# SFT_model_dirに学習後のtokenizerを保存
#tokenizer.save_pretrained(SFT_model_dir) 
# SFT_model_dirに学習後のモデルを保存
model.save_pretrained(SFT_model_dir)     
time_end = time.time()
# convert second to hour, minute and seconds
end_time = (time_end - time_start)
hour = end_time // 3600
minute = (end_time % 3600) // 60
second = (end_time % 3600 % 60)
time_str=str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
print(time_str)

with open(SFT_model_dir+"time_data.txt", 'w') as f:
    f.write("learn "+str(i)+" "+flow_lst[i]+" "+time_str+"\n")

#メモリやGPUの開放
del dataset
del model
del tokenizer
import torch
torch.cuda.empty_cache()