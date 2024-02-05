import peft
################################################################################
# LoRA parameters
################################################################################

# LoRA rank dimension
lora_r = 64
# Alpha parameter for LoRA scaling
lora_alpha = 2*lora_r
# Dropout probability for LoRA layers
lora_dropout = 0.1

bias="none"
task_type=peft.TaskType.CAUSAL_LM
target_modules=["q_proj","k_proj","v_proj","o_proj"]
fan_in_fan_out=None

################################################################################
# TrainingArguments parameters
################################################################################

# Output directory where the model predictions and checkpoints will be stored
#output_dir
# Number of training epochs
num_train_epochs = 10
# Enable fp16/bf16 training (set bf16 to True with an A100)
fp16 = False #True
bf16 = False
# Batch size per GPU for training
#per_device_train_batch_size = 2
per_device_train_batch_size = 4
# Batch size per GPU for evaluation
#per_device_eval_batch_size = 2
per_device_train_batch_size = 4
# Number of update steps to accumulate the gradients for
gradient_accumulation_steps = 1
# Enable gradient checkpointing
gradient_checkpointing = True
# Maximum gradient normal (gradient clipping)
max_grad_norm = 0.3
# Initial learning rate (AdamW optimizer)
learning_rate = 2e-5
# Weight decay to apply to all layers except bias/LayerNorm weights
weight_decay = 0.01
# Optimizer to use
optim = "paged_adamw_32bit"
# Learning rate schedule (constant a bit better than cosine)
lr_scheduler_type = "constant"
# Number of training steps (overrides num_train_epochs)
max_steps = -1
# Ratio of steps for a linear warmup (from 0 to learning rate)
warmup_ratio = 0.03
# Group sequences into batches with same length
# Saves memory and speeds up training considerably
group_by_length = True
# Save checkpoint every X updates steps
save_steps = 100
# Log every X updates steps
logging_steps = 10

report_to="wandb"

# warmup_steps=20,
# save_strategy="steps",
# save_total_limit=10,
# evaluation_strategy="no",
# logging_dir="logs",
# gradient_checkpointing=True,
# push_to_hub=False,

################################################################################
# SFT parameters
################################################################################

dataset_text_field="text"
# Maximum sequence length to use
max_seq_length = None
# Pack multiple short examples in the same input sequence to increase efficiency
packing = False
# Load the entire model on the GPU 0
device_map = {"": 0}

#formatting_func=formatting_prompts_func,#あらかじめプロンプトを決めて加工まで終わっていればいらない
formatting_func=None
data_collator=None

# Check GPU compatibility with bfloat16
# if compute_dtype == torch.float16 and use_4bit:
#     major, _ = torch.cuda.get_device_capabilitfy()
#     if major >= 8:
#         print("=" * 80)
#         print("Your GPU supports bfloat16: accelerate training with bf16=True")
#         print("=" * 80)