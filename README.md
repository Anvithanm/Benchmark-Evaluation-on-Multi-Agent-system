# Benchmark Evaluation on Multi-Agent System (MaAS)

## Overview

This project evaluates the **MaAS (Multi-agent Architecture Search)** system on two popular benchmarks to understand how well a locally-running multi-agent LLM pipeline performs on both structured math and broad knowledge tasks.

**Two experiments were run:**
- **Experiment 1** — GSM8K (Grade School Math)
- **Experiment 2** — MMLU (Massive Multitask Language Understanding)

---

## Setup & Utilities

- **Model backend**: [Ollama](https://ollama.ai) running `qwen2.5:7b` locally
- **Dataset prep**: [`download_mmlu_data.py`](download_mmlu_data.py) and [`dataset_loading_math.py`](dataset_loading_math.py)
- **Connectivity test**: [`test_ollama.py`](test_ollama.py)
- **Result analysis**: [`analyze_results.py`](analyze_results.py)

---

## Files Created & Modified

### New Files

| File | Purpose |
|------|---------|
| `download_mmlu_data.py` | Downloads MMLU dataset from Hugging Face |
| `dataset_loading_math.py` | Loads GSM8K dataset in JSONL format |
| `test_ollama.py` | Tests connectivity and model response via Ollama |
| `analyze_results.py` | Result analysis and visualization |
| `maas/ext/maas/benchmark/mmlu.py` | MMLU benchmark implementation for MaAS |

### Modified Files

| File | Changes |
|------|---------|
| `operator.py` (train/test) | Added `ScEnsemble` error handling and validation |
| `action_node.py` | Enhanced logging for debugging LLM responses |
| `gsm8k.py` | Improved error logging for GSM8K processing |
| `benchmark.py` | Fixed tensor type mismatches |
| `evaluator.py` | Added registration for MMLU benchmark |
| `experiment_configs.py` | Added configuration entries for MMLU |

---

## Experiment 1 — GSM8K (Grade School Math)

The goal here was to run MaAS on grade school arithmetic word problems and see where it succeeds and where it falls flat. Math like this is deceptively tricky for LLMs — the calculations aren't hard, but the reading comprehension is.

### Benchmark Details

- **Dataset**: [GSM8K / Scale Math](https://github.com/scaleapi/gsm1k_eval)
- **Paper**: [arxiv.org/pdf/2405.00332](https://arxiv.org/pdf/2405.00332)
- **Leaderboard**: [scale.com/leaderboard/math](https://scale.com/leaderboard/math)
- **Difficulty**: Fifth-grade arithmetic with multi-step reasoning

### Configuration

- **Model**: `qwen2.5:7b` (local LLM via Ollama)
- **Sample Size**: 100 unique problems × 3 repetitions = 300 evaluations
- **Operators available**:
  - `Generate` — basic answer generation
  - `GenerateCoT` — chain-of-thought reasoning
  - `MultiGenerateCoT` — multiple CoT generations
  - `Programmer` — Python code generation and execution
  - `SelfRefine` — solution refinement
  - `ScEnsemble` — self-consistency ensemble voting

### Results

| Metric | Value |
|--------|-------|
| **Accuracy** | **91.33%** (274/300 correct) |
| Unique problems tested | 100 |
| Failed problems | 13 unique |
| Most effective operator | `Programmer` |
| Best combination | `MultiGenerateCoT → ScEnsemble → Programmer` |

### Terminal Output (Final Score)

```
2025-11-24 12:07:47.831 | INFO | benchmark:save_results_to_csv - Results saved to .../GSM8K/train/round_1/0.91333_20251124_120747.csv
2025-11-24 12:07:47.831 | INFO | benchmark:run_evaluation - Average score on GSM8K dataset: 0.91333
2025-11-24 12:07:47.835 | INFO | benchmark:run_evaluation - Saved controller parameters to .../GSM8K/train/round_1/GSM8K_controller_sample3.pth
2025-11-24 12:07:47.836 | INFO | benchmark:run_evaluation - Successfully Finish Training
```

---

## 3 Easiest Problems Where MaAS Failed

These failures are interesting because the math itself is simple — the mistakes are almost always in how the problem was read, not how the numbers were crunched.

### 1. Bethany's Shoe Discount

**Question**: "Bethany put aside $50 to buy shoes. They were on sale and she saved $7.50. What percent was the discount?"

- **Expected**: 15%
- **MaAS got**: 13.04%

**What went wrong**: MaAS calculated `7.5 / 57.5 × 100 ≈ 13.04%` — treating the *sale price* as the base instead of the *original price*. The correct calculation is `7.5 / 50 × 100 = 15%`.

**Fix**: Add percentage-base validation, or a specialized operator that explicitly identifies what the denominator should be.

---

### 2. George's Sheep Shaving

**Question**: "120 sheep, 20 min each, 2 workers, 5 hours/day. How many days to shave all sheep?"

- **Expected**: 4 days
- **MaAS got**: 80

**What went wrong**: The correct path is `(120 × 20) / 2 = 1,200 min → 20 hours → 4 days`. MaAS returned 80, which suggests it used 30 minutes/hour instead of 60 during unit conversion.

**Fix**: Better unit conversion handling in the `Programmer` operator.

---

### 3. Gail's Gym Drinks

**Question**: Gail buys 1+2+3+4+4 = 14 drinks per week over 5 days. She wants 20 total. After week 1 she has 14. She needs 6 more (Mon: +1, Tue: +2, Thu: +3 = done). How many *days* did she visit?

- **Expected**: 8 days
- **MaAS got**: 10

**What went wrong**: Likely divided 20 / 2 = 10 (using average drinks/day). The system didn't simulate the weekly pattern incrementally.

**Fix**: A dedicated cumulative-sum operator would help with this kind of sequential pattern problem.

---

## 3 Hardest Problems Where MaAS Succeeded

These problems have a lot of moving parts — multiple categories, interdependent variables, or mixed fractions. MaAS nailed them, mostly thanks to the `Programmer` operator turning messy word problems into clean code.

### 1. Easter Egg Hunt Fundraiser

**Question**: 5000 eggs across 4 color categories, each representing different donation amounts, minus candy costs and bounce house rentals. How much profit?

- **Expected**: $137,655 ✓
- **Workflow**: `MultiGenerateCoT → ScEnsemble → Programmer`

The combination of multiple reasoning paths, ensemble voting, and code verification meant no arithmetic mistakes slipped through.

---

### 2. Choir Field Trip Budget

**Question**: 183 members paying 7 different ticket prices. Total to collect?

- **Expected**: $69,137 ✓
- **Workflow**: `GenerateCoT → Programmer → Code Execution`

The `Programmer` operator just wrote a Python script that summed each category — elegant and accurate.

---

### 3. Manufacturing Parts Inventory

**Question**: 8 interdependent parts (screws > bolts, studs from screws, nuts from studs…). Given 47 bolts, find total parts.

- **Expected**: 4,554 ✓
- **Workflow**: `GenerateCoT → Programmer → Code Execution`

`GenerateCoT` identified the dependency chain. `Programmer` computed each variable in sequence. No room for mental arithmetic errors.

---

## Key Takeaways (Experiment 1)

### Where MaAS Struggles
- **Percentage base errors** — picks the wrong denominator
- **Unit conversions** — time and measurement calculations go wrong
- **Reading comprehension** — misses conjunctions, compound subjects
- **Pattern recognition** — cumulative sum problems with weekly cycles

### Where MaAS Shines
- **Code generation** — `Programmer` is extremely reliable for multi-step arithmetic
- **Ensemble voting** — `ScEnsemble` catches errors when multiple paths are consistent
- **Large numbers** — code execution eliminates human arithmetic slip-ups
- **Structured problems** — clear variable relationships play to MaAS's strengths

### Operator Effectiveness
| Operator | Best For |
|----------|---------|
| `Programmer` | Multi-step math, large numbers, dependency chains |
| `ScEnsemble` | Ambiguous or complex problems with multiple solution paths |
| `GenerateCoT` | Problem decomposition (but prone to arithmetic errors) |
| `Generate` | Simple problems — struggles with careful reading |

---

## Reproduction (Experiment 1)

```bash
cd week_10/MaAS

python -m examples.maas.optimize \
  --dataset scale_math \
  --round 1 \
  --sample 100 \
  --exec_model_name "qwen2.5:7b"
```

---

## Experiment 2 — MMLU (Massive Multitask Language Understanding)

MMLU is a much harder benchmark to crack with a local 7B model. It covers 57 subjects — from abstract algebra and law to US history and medicine — and requires genuine conceptual understanding, not just arithmetic. Spoiler: 56% accuracy on a 25%-random-chance MCQ test is decent, but there's a big gap from the GSM8K numbers.

### Benchmark Details

- **Dataset**: [cais/mmlu on Hugging Face](https://huggingface.co/datasets/cais/mmlu)
- **Paper**: [Measuring Massive Multitask Language Understanding](https://arxiv.org/pdf/2009.03300)
- **GitHub**: [hendrycks/test](https://github.com/hendrycks/test)
- **Leaderboard**: [Kaggle MMLU Leaderboard](https://www.kaggle.com/benchmarks/open-benchmarks/mmlu)

### Adapting MaAS for MCQ

MMLU requires a single letter answer (A/B/C/D) instead of open-ended output, so a few things had to be changed:

1. **Operators** — `Generate`, `GenerateCoT`, and `ScEnsemble` were modified to return a structured output with an answer letter and optional reasoning
2. **Benchmark class** — implemented exact-match evaluation on answer letters
3. **Config** — registered `MMLU` in `experiment_configs.py` and `evaluator.py`

### Results

| Metric | Value |
|--------|-------|
| **Accuracy** | **56.00%** |
| Total questions | 200 sampled |
| Model | `qwen2.5:7b` |

### Terminal Output (Final Score)

```
2025-11-26 18:20:59.062 | INFO | benchmark:save_results_to_csv - Results saved to .../MMLU/train/round_1/0.56000_20251126_182059.csv
2025-11-26 18:20:59.062 | INFO | benchmark:run_evaluation - Average score on MMLU dataset: 0.56000
2025-11-26 18:20:59.066 | INFO | benchmark:run_evaluation - Saved controller parameters to .../MMLU/train/round_1/MMLU_controller_sample2.pth
2025-11-26 18:20:59.066 | INFO | benchmark:run_evaluation - Successfully Finish Training
```

---

## 3 Easiest Failures (Experiment 2)

Most failures came from Abstract Algebra — a tough subject for a 7B model to reason through precisely.

### Example 1 — Factor Groups & Normal Subgroups

**Question**: Statement 1: A factor group of a non-Abelian group is non-Abelian. Statement 2: If K is normal in H and H is normal in G, then K is normal in G.

- **Correct**: B (both false)
- **MaAS got**: D (Statement 1 false, Statement 2 true)

The model fell into a classic trap — assuming normality is transitive (it isn't). Statement 2 is false, but the model hallucinated a theorem saying otherwise.

---

### Example 2 — Elements of Order 15

**Question**: Statement 1: A group with an element of order 15 must have at least 8 elements of order 15. Statement 2: If a group has more than 8 elements of order 15, it must have at least 16.

- **Correct**: A (both true)
- **MaAS got**: C (Statement 1 true, Statement 2 false)

The model correctly applied Euler's totient (φ(15) = 8) for Statement 1 but failed the combinatorial reasoning for Statement 2.

---

### Example 3 — Homomorphic Images

**Question**: Statement 1: Every homomorphic image of G is isomorphic to a factor group of G. Statement 2: The homomorphic images and factor groups of G are the same (up to isomorphism).

- **Correct**: A (both true)
- **MaAS got**: C (Statement 1 true, Statement 2 false)

Inconsistency in the model's own reasoning — it accepted the specific case (Statement 1) but rejected the general equivalence (Statement 2), which is essentially the same thing.

---

## 3 Hardest Successes (Experiment 2)

### Example 1 — Field Extension Degree

**Question**: Find the degree of Q(√2, √3, √18) over Q.

- **Correct**: 4 ✓
- **Workflow**: `GenerateCoT → Answer`

The model correctly identified that √18 = 3√2, so it doesn't extend the field further. Then it computed [Q(√2, √3) : Q] = 4.

---

### Example 2 — Index of a Subgroup in S₅

**Question**: Let p = (1 2 5 4)(2 3) in S₅. Find the index of ⟨p⟩ in S₅.

- **Correct**: C ✓
- **Workflow**: `GenerateCoT → Answer`

The model composed the permutations correctly, found the disjoint cycle form, determined the order of the element, and applied Lagrange's theorem to get the index.

---

### Example 3 — Zeros of a Polynomial in Z₅

**Question**: Find all zeros of x⁵ + 3x³ + x² + 2x in Z₅.

- **Correct**: D ✓
- **Workflow**: `GenerateCoT → Answer`

The model applied Fermat's Little Theorem (x⁵ = x in Z₅) to simplify, then tested each value 0–4. Clean and correct.

---

## Overall Conclusion

| Metric | GSM8K | MMLU |
|--------|-------|------|
| **Accuracy** | **91.33%** | **56.00%** |
| **Best Operator** | `Programmer` | `GenerateCoT` |
| **Main Weakness** | Reading comprehension | Theorem verification |

MaAS with `qwen2.5:7b` is genuinely strong at mathematical computation — when problems can be turned into code, accuracy is very high. The multi-agent architecture (especially `Programmer + ScEnsemble`) adds real value.

MMLU tells a different story. At 56%, the system is well above random chance (25%), but abstract conceptual reasoning — especially in advanced mathematics and formal logic — is clearly hard for a local 7B model. Adding a TheoremVerifier operator or retrieval-augmented reasoning could help narrow that gap.

**The core lesson**: code execution compensates for arithmetic errors beautifully, but it can't substitute for deep domain knowledge.

---

## Citation

**MaAS**
```bibtex
@article{zhang2025agenticsupernet,
  title={Multi-agent Architecture Search via Agentic Supernet},
  author={Zhang, Guibin and Niu, Luyang and Fang, Junfeng and Wang, Kun and Bai, Lei and Wang, Xiang},
  journal={arXiv preprint arXiv:2502.04180},
  year={2025}
}
```

**MMLU**
```bibtex
@article{hendryckstest2021,
  title={Measuring Massive Multitask Language Understanding},
  author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
  journal={ICLR},
  year={2021}
}
```

**GSM8K / Scale Math**
```bibtex
@article{scalemath2024,
  title={GSM1K: Grade School Math Evaluation},
  author={Scale AI},
  year={2024}
}
```
