"""
Download and prepare MMLU dataset
- Downloads 'cais/mmlu' (all subjects)
- Formats answers from 0-3 to A-D
- Saves first 100 examples for training
"""
from datasets import load_dataset
import json
import os

print("Downloading MMLU dataset...")
# "all" loads all subjects. split="test" is standard for MMLU evaluation
dataset = load_dataset("cais/mmlu", "all", split="test")

print(f"Total questions: {len(dataset)}")

train_data = []
# Take first 100 for training/testing purposes
for i, item in enumerate(dataset):
    if i >= 100:
        break
    
    # MMLU answer is an integer 0-3. Convert to A-D.
    answer_idx = item['answer']
    answer_letter = chr(65 + answer_idx)  # 0->A, 1->B, 2->C, 3->D
    
    clean_item = {
        'question': item['question'],
        'choices': item['choices'],
        'answer': answer_letter,
        'subject': item.get('subject', 'Unknown')
    }
    train_data.append(clean_item)

print(f"Selected for training: {len(train_data)}")

# Create directory if it doesn't exist
output_path_train = "d:/neu-self-improve-ai/week_10/MaAS/maas/ext/maas/data/mmlu_train.jsonl"
output_path_test = "d:/neu-self-improve-ai/week_10/MaAS/maas/ext/maas/data/mmlu_test.jsonl"
os.makedirs(os.path.dirname(output_path_train), exist_ok=True)

# Save train file
with open(output_path_train, 'w', encoding='utf-8') as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Save test file (using same data for now for simplicity, or could slice differently)
with open(output_path_test, 'w', encoding='utf-8') as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"✅ Saved to: {output_path_train}")
print(f"✅ Saved to: {output_path_test}")

# Show sample
print("\nSample question:")
sample = train_data[0]
print(f"Question: {sample['question'][:200]}...")
print(f"Choices: {sample['choices']}")
print(f"Answer: {sample['answer']}")
print(f"Subject: {sample.get('subject', 'N/A')}")
