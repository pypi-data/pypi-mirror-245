import os
import time

import ainyan.models
import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    # HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)

from peft import LoraConfig, PeftModel
from trl import SFTTrainer
import configparser
import argparse


def main():
    parser = argparse.ArgumentParser(description='Training facilitator')
    parser.add_argument('--config', metavar='config', required=True,
                        help='the path to the ini file used for training')
    parser.add_argument('--phase', choices=['train', 'merge', 'upload'], metavar='phase', required=False,
                        help='the phase to start with')
    args = parser.parse_args()

    training_file = args.config
    phase = "train" if args.phase is None else args.phase

    config = configparser.ConfigParser()
    config.read(training_file)

    training = config["training"]
    model_name = training["model"]

    # dataset_name = training["dataset"]
    newmodel_finalname = training["finalname"]
    new_model_name = newmodel_finalname + "_training"
    os.environ['AWS_PROFILE'] = training["aws_profile"]

    print(f'Start Time {time.time()}\nSettings are from {training_file} on base model {model_name} from phase {phase}')

    model = loadModelWithBitsAndBytesConfig(model_name)
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    if phase == "train":
        train(model, model_name, new_model_name, tokenizer, training)
        merge(model_name, new_model_name, newmodel_finalname, tokenizer)
        upload(config, newmodel_finalname)

    if phase == "merge":
        merge(model_name, new_model_name, newmodel_finalname, tokenizer)
        upload(config, newmodel_finalname)

    if phase == "upload":
        upload(config, newmodel_finalname)

    print(f'Finished at{time.time()}:\t{training_file}. Model saved is: {newmodel_finalname}')


def loadModelWithBitsAndBytesConfig(model_name):
    # BitsAndBytesConfig
    # use_4bit = True
    compute_dtype = getattr(torch, "float16")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=False,
    )
    # Load the entire model on the GPU 0
    # TODO: device_map needs to take all the GPUs
    device_map = {"": 0}
    # base model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map=device_map
    )
    return model


def train(model, model_name, new_model_name, tokenizer, training):

    train_dataset_name = training["train_dataset"]
    print(f'Using Train Dataset {train_dataset_name}')
    train_dataset = load_from_disk(train_dataset_name)
    print(train_dataset[:1])

    eval_dataset_name = training.get("train_dataset", fallback=None)
    eval_dataset = None if eval_dataset_name is None else load_from_disk(eval_dataset_name)

    if eval_dataset_name is None:
        print(f'Not using eval dataset')
    else:
        print(f'Using Eval Dataset {eval_dataset_name}')


    # Load LoRA configuration
    lora_r = 64
    lora_alpha = 16
    lora_dropout = 0.1
    peft_config = LoraConfig(
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        r=lora_r,
        bias="none",
        task_type="CAUSAL_LM",
    )
    # training arguments
    # Output directory where the model predictions and checkpoints will be stored
    # output_dir = "./results"
    output_dir = "./" + model_name + "_training"
    gradient_checkpointing = True

    # Number of training epochs
    # num_train_epochs = 1
    # Enable fp16/bf16 training (set bf16 to True with an A100)
    # fp16 = training.getboolean("fp16", fallback=False)
    # bf16 = training.getboolean("bf16", fallback=False)
    # Batch size per GPU for training
    # per_device_train_batch_size = training.getint("per_device_train_batch_size", fallback=2)
    # Batch size per GPU for evaluation
    # per_device_eval_batch_size = 2
    # Number of update steps to accumulate the gradients for
    # gradient_accumulation_steps = 1
    # Enable gradient checkpointing
    # gradient_checkpointing = True
    # Maximum gradient normal (gradient clipping)
    # max_grad_norm = 0.3
    # Initial learning rate (AdamW optimizer)
    # learning_rate = 2e-4
    # learning_rate = 2e-3
    # learning_rate = training.getfloat("learning_rate", fallback=2e-4)
    # Weight decay to apply to all layers except bias/LayerNorm weights
    # weight_decay = training.getfloat("weight_decay", fallback=0.001)
    # Optimizer to use
    optim = "paged_adamw_32bit"
    # Learning rate schedule (constant a bit better than cosine)
    lr_scheduler_type = "constant"
    # Number of training steps (overrides num_train_epochs)
    # max_steps = -1
    # max_steps = 100
    # max_steps = training.getint("max_steps", fallback=-1)
    # Ratio of steps for a linear warmup (from 0 to learning rate)
    # warmup_ratio = training.getfloat("warmup_ratio", fallback=0.03)
    # Group sequences into batches with same length
    # Saves memory and speeds up training considerably
    group_by_length = True
    # Save checkpoint every X updates steps
    # save_steps = training.getint("save_steps", fallback=25)
    # Log every X updates steps
    # logging_steps =

    training_arguments = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=training.getint("num_train_epochs", fallback=1),
        per_device_train_batch_size=training.getint("per_device_train_batch_size", fallback=2),
        gradient_accumulation_steps=training.getint("gradient_accumulation_steps", fallback=1),
        optim=optim,
        save_steps=training.getint("save_steps", fallback=25),
        logging_steps=training.getint("logging_steps", fallback=10),
        learning_rate=training.getfloat("learning_rate", fallback=2e-4),
        weight_decay=training.getfloat("weight_decay", fallback=0.001),
        fp16=training.getboolean("fp16", fallback=False),
        bf16=training.getboolean("bf16", fallback=False),
        do_eval=False if eval_dataset_name is None else True,
        do_predict=False,
        do_train=True,
        max_grad_norm=training.getfloat("max_grad_norm", fallback=0.3),
        max_steps=training.getint("max_steps", fallback=-1),
        warmup_ratio=training.getfloat("warmup_ratio", fallback=0.03),
        group_by_length=group_by_length,
        lr_scheduler_type=lr_scheduler_type,
        # report_to="tensorboard"
    )

    # https://stackoverflow.com/questions/75786601/how-to-convert-trainingarguments-object-into-a-json-file
    print("TRAINING CONFIG\n:" + training_arguments.to_json_string())

    # SFT parameters
    # Maximum sequence length to use
    max_seq_length = None
    # Pack multiple short examples in the same input sequence to increase efficiency
    packing = False
    # Load the entire model on the GPU 0
    # device_map = {"": 0}
    # Set supervised fine-tuning parameters
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        tokenizer=tokenizer,
        args=training_arguments,
        packing=packing,
    )
    
    trainer.train()
    trainer.model.save_pretrained(new_model_name)
    tokenizer.save_pretrained(new_model_name)

    if training.get("empty_cache"):
        torch.cuda.empty_cache()


def upload(config, newmodel_finalname):
    s3_config = config["s3"]
    training = config["training"]
    if s3_config.getboolean("upload") is True:
        ainyan.models.model_to_s3(newmodel_finalname, s3_config["bucket"], training["aws_profile"])


def merge(model_name, new_model_name, newmodel_finalname, tokenizer):
    # merge
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    # model = loadModelWithBitsAndBytesConfig(model_name)
    model = PeftModel.from_pretrained(model, new_model_name)
    model = model.merge_and_unload()

    # save
    model.save_pretrained(newmodel_finalname)
    tokenizer.save_pretrained(newmodel_finalname)


if __name__ == '__main__':
    main()
