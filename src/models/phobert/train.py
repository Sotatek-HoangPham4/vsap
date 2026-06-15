from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import numpy as np
import evaluate
from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
)

from .tokenizer import get_tokenizer

import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")


accuracy = evaluate.load("accuracy")
f1 = evaluate.load("f1")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)

    return {
        "accuracy": accuracy.compute(predictions=preds, references=labels)["accuracy"],
        "f1": f1.compute(predictions=preds, references=labels, average="macro")["f1"],
    }


def tokenize_fn(tokenizer):
    def fn(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            padding=True,
            max_length=256,
        )
    return fn


def train_phobert(model_name, train_dataset, test_dataset):

    tokenizer = get_tokenizer(model_name)

    train_dataset = train_dataset.map(tokenize_fn(tokenizer), batched=True)
    test_dataset = test_dataset.map(tokenize_fn(tokenizer), batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=3
    )

    args = TrainingArguments(
        output_dir=f"./outputs/{model_name.replace('/', '_')}",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir="./logs",
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )

    trainer.train()

    return trainer.evaluate()