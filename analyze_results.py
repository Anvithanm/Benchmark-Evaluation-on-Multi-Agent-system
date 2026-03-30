import csv
import re

# Read the CSV file
with open(r'd:\neu-self-improve-ai\week_10\MaAS\maas\ext\maas\scripts\optimized\GSM8K\train\round_1\0.91333_20251124_120747.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Filter unique problems (remove duplicates from repetitions)
unique_problems = {}
for row in data:
    q = row['question']
    if q not in unique_problems:
        unique_problems[q] = row

# Separate failures and successes
failures = []
successes = []

for q, row in unique_problems.items():
    score = float(row['score'])
    expected = float(row['expected_output']) if row['expected_output'] else 0
    
    # Calculate problem complexity (simple heuristic: word count + number count)
    word_count = len(q.split())
    number_count = len(re.findall(r'\d+', q))
    complexity = word_count + (number_count * 2)  # Numbers add more complexity
    
    row['complexity'] = complexity
    row['word_count'] = word_count
    
    if score == 0.0:
        failures.append(row)
    else:
        successes.append(row)

# Sort failures by complexity (easiest first)
failures_sorted = sorted(failures, key=lambda x: x['complexity'])

# Sort successes by complexity (hardest first)
successes_sorted = sorted(successes, key=lambda x: x['complexity'], reverse=True)

print("="*80)
print(f"TOTAL UNIQUE PROBLEMS: {len(unique_problems)}")
print(f"FAILURES: {len(failures)}")
print(f"SUCCESSES: {len(successes)}")
print("="*80)

print("\n" + "="*80)
print("5 EASIEST FAILURES (sorted by complexity)")
print("="*80)
for i, row in enumerate(failures_sorted[:5], 1):
    print(f"\n{i}. QUESTION (Complexity: {row['complexity']}, Words: {row['word_count']}):")
    print(f"   {row['question'][:200]}...")
    print(f"   Expected: {row['expected_output']}")
    print(f"   Predicted: {row['prediction'][:100] if len(row['prediction']) < 100 else row['prediction'][:100] + '...'}")

print("\n" + "="*80)
print("5 HARDEST SUCCESSES (sorted by complexity)")
print("="*80)
for i, row in enumerate(successes_sorted[:5], 1):
    print(f"\n{i}. QUESTION (Complexity: {row['complexity']}, Words: {row['word_count']}):")
    print(f"   {row['question'][:200]}...")
    print(f"   Expected: {row['expected_output']}")
    print(f"   Predicted: {row['prediction'][:100] if len(row['prediction']) < 100 else row['prediction'][:100] + '...'}")
