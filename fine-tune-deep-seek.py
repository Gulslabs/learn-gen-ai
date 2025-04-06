#Pre-requisites: 
# Create an account in Kaggle.com and work on kaggle editor
# Create an account on Weigts and biases. 
# We use unsloth for model download. 
#Step 1: Get secrets from Kaggle and Weights and Biases. 
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
hf_token = user_secrets.get_secret("HUGGINGFACE_TOKEN")

import wandb
wb_token = user_secrets.get_secret("wandb")
wandb.login(key=wb_token)
run = wandb.init(
    project='Fine-tune-DeepSeek-R1-Distill-Llama-8B on Medical COT Dataset', 
    job_type="training", 
    anonymous="allow"
)

#Step 3: load the Unsloth version of DeepSeek-R1-Distill-Llama-8B; with 4-bit quantization. 
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/DeepSeek-R1-Distill-Llama-8B",
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
    token = hf_token, 
)

# Step 4: Try a quick inference. (Optional)
medi_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. 
Write a response that appropriately completes the request. Before answering, think carefully about the question and create a step-by-step chain of thoughts to ensure a logical and accurate response.
### Instruction:
You are a medical expert with advanced knowledge in clinical reasoning, diagnostics, and treatment planning. 
Please answer the following medical question. 

### Question:
{}

### Response:
<think>{}"""

question = "A 61-year-old woman with a long history of involuntary urine loss during activities like coughing or sneezing but no leakage at night undergoes a gynecological exam and Q-tip test. Based on these findings, what would cystometry most likely reveal about her residual volume and detrusor contractions?"

FastLanguageModel.for_inference(model) 
# If you are without a GPU; remove the to cuda option. 
inputs = tokenizer([medi_prompt.format(question, "")], return_tensors="pt").to("cuda")
outputs = model.generate(
    input_ids=inputs.input_ids,
    attention_mask=inputs.attention_mask,
    max_new_tokens=1200,
    use_cache=True,
)
response = tokenizer.batch_decode(outputs)
print(response[0].split("### Response:")[1])
# The reasoning process is encapsulated within the <think></think> tags.

# Step 5: Create a Training Prompt
trainee_medi_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. 
Write a response that appropriately completes the request. 
Before answering, think carefully about the question and create a step-by-step chain of thoughts to ensure a logical and accurate response.

### Instruction:
You are a medical expert with advanced knowledge in clinical reasoning, diagnostics, and treatment planning. 
Please answer the following medical question. 

### Question:
{}

### Response:
<think>
{}
</think>
{}"""

# Step 6: A Utility Function to format the question. 
EOS_TOKEN = tokenizer.eos_token  # We must add End of Sequence Token. 

def formatting_prompts_func(examples):
    inputs = examples["Question"]
    cots = examples["Complex_CoT"]
    outputs = examples["Response"]
    texts = []
    for input, cot, output in zip(inputs, cots, outputs):
        text = trainee_medi_prompt.format(input, cot, output) + EOS_TOKEN
        texts.append(text)
    return {
        "text": texts,
    }

# Step 7: Create a Training Dataset. Load 500 dataset from medical-o1-reasoning-SFT. 
from datasets import load_dataset
dataset = load_dataset("FreedomIntelligence/medical-o1-reasoning-SFT", "en", split="train[:500]", trust_remote_code=True)
dataset = dataset.map(formatting_prompts_func, batched=True)
dataset = dataset.shuffle(seed=42)
dataset["text"][0]

# Step 8: Step the model for fine-tunning. Creates a PEFT (Parameter-Efficient Fine-Tuning) version of the language model with LoRA (Low-Rank Adaptation) configuration.
"""
target_modules : List of module names to apply LoRA to. Here we are targeting attention layers and MLP components:
    - "q_proj", "k_proj", "v_proj", "o_proj": Attention layer projections
    - "gate_proj", "up_proj", "down_proj": MLP components
"""
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    lora_alpha=16, # Scaling factor. Higher values increase the impact of LoRA updates.
    lora_dropout=0,  
    bias="none",  
    use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context. Enable graident checkpoint to reduce memory usage. 
    random_state=3407, # Random seed for reproducibility. 
    use_rslora=False,  # Do not use Rank-Stable Lora. 
    loftq_config=None,
)

# Step 9: Train the model.
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
max_seq_length = 2048 
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        # Use num_train_epochs = 1, warmup_ratio for full training runs!
        warmup_steps=5,
        max_steps=60,
        learning_rate=2e-4,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
    ),
)

trainer_stats = trainer.train()

# Step 10: Model Inference after training(tunning)
question = "A 61-year-old woman with a long history of involuntary urine loss during activities like coughing or sneezing but no leakage at night undergoes a gynecological exam and Q-tip test. Based on these findings, what would cystometry most likely reveal about her residual volume and detrusor contractions?"

FastLanguageModel.for_inference(model) # Unsloth has 2x faster inference!
# If you are without a GPU; remove the to cuda option. 
inputs = tokenizer([medi_prompt.format(question, "")], return_tensors="pt").to("cuda")
outputs = model.generate(
    input_ids=inputs.input_ids,
    attention_mask=inputs.attention_mask,
    max_new_tokens=1200,
    use_cache=True,
)
response = tokenizer.batch_decode(outputs)
print(response[0].split("### Response:")[1])

# Step 11: Save the model.
new_model_local = "DeepSeek-R1-Medical-COT-Distill-Llama-8B" 
model.save_pretrained(new_model_local)
tokenizer.save_pretrained(new_model_local)  

# Step 12: Push the model to hugging face. 
new_model_online = "guls/DeepSeek-R1-Medical-COT-Distill-Llama-8B"
model.push_to_hub(new_model_online)
tokenizer.push_to_hub(new_model_online)
model.push_to_hub_merged(new_model_online,  tokenizer, save_method="merged_16bit")