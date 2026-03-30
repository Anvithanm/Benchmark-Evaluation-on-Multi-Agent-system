# Create a file: setup_gsm1k.py
from datasets import load_dataset
import json

# Download GSM1k
print("Downloading GSM1k dataset...")
dataset = load_dataset("ScaleAI/gsm1k")

print(f"Total problems in GSM1k: {len(dataset['test'])}")

# Split 80/20 (or choose your ratio)
split_dataset = dataset['test'].train_test_split(test_size=0.2, seed=42)

train_data = split_dataset['train']  # 968 problems (80%)
test_data = split_dataset['test']    # 242 problems (20%)

print(f"Train: {len(train_data)} problems")
print(f"Test: {len(test_data)} problems")

# Save train set
print("\nSaving train set...")
with open('gsm1k_train.jsonl', 'w') as f:
    for item in train_data:
        f.write(json.dumps(item) + '\n')

# Save test set
print("Saving test set...")
with open('gsm1k_test.jsonl', 'w') as f:
    for item in test_data:
        f.write(json.dumps(item) + '\n')

print("\n✅ GSM1k dataset split and saved!")
print(f"   Train: maas/ext/maas/data/gsm1k_train.jsonl (968 problems)")
print(f"   Test:  maas/ext/maas/data/gsm1k_test.jsonl (242 problems)")