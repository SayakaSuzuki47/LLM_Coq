### Fine-TuningもしくはLoRAのlearnファイルのprint('start')以降を下記で書き換える ###

#学習を再開したいところのチェックポイントのパスを書く．
dir_path=#モデルを保存している場所のパス
checkpoint = dir_path + "checkpoint-200"

print('start')
time_start = time.time()
model.config.use_cache = False
trainer.train(resume_from_checkpoint=checkpoint)
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