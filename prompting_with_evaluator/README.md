# Prompting with PromptEvaluator class · Lab notebooks

Where the course consolidates everything into a reusable `PromptEvaluator` class. This is the "production-shape" of the eval workflow.

## Files

| File | Purpose |
|------|---------|
| `001_prompting.ipynb` | Start of the lab · build the `PromptEvaluator` class step by step |
| `002_prompting_completed.ipynb` | Reference solution · full working class with all methods |
| `prompt_evaluator.py` | Standalone Python module · same class extracted for reuse outside notebooks |

## What the `PromptEvaluator` class does

A single object that wraps the full eval workflow:

```python
evaluator = PromptEvaluator(max_concurrent_tasks=2)

# 1. Generate synthetic dataset
dataset = evaluator.generate_dataset(
    task_description="Extract topics from scholarly article into JSON array",
    prompt_inputs_spec={"content": "One paragraph of text..."},
    output_file="dataset.json",
    num_cases=4,
)

# 2. Run prompt under test against dataset
# 3. Grade outputs by model
# 4. Render an evaluation report
results = evaluator.run_evaluation(...)
```

## Methods (notebook + standalone module)

| Method | Stage |
|--------|-------|
| `generate_dataset()` | Synthesize test cases (Haiku · cheap, fast) |
| `generate_test_case()` | Generate one case at a time |
| `generate_unique_ideas()` | Brainstorm variation seeds for diversity |
| `run_prompt()` | Execute prompt under test (Sonnet · the model you'll deploy) |
| `run_test_case()` | Single end-to-end case |
| `grade_output()` / `grade_by_model()` | Model-graded scoring with reasoning before number |
| `run_evaluation()` | Loop over the whole dataset |
| `generate_prompt_evaluation_report()` | Final aggregated report |
| `render()` | Pretty-print results |

## Why this pattern matters

The `PromptEvaluator` class is what separates **someone who watched a prompting tutorial** from **someone who ships prompts to production**. Same pattern Anthropic uses internally to validate Claude itself.

## Production application at H3L Consulting

We're integrating this `PromptEvaluator` into the H3L Diagnostics pipeline to regression-test our auditor prompts:

- `task_description` = "Classify which of the 28 H3L operational waste categories apply to this company"
- `prompt_inputs_spec` = the Supercias data fields (RUC, sector CIIU, ROE, liquidez, empleados, ingresos)
- `dataset` = 50 frozen golden cases hand-labeled by us
- `target_model` = `claude-sonnet-4-5` (the one we deploy)
- `grader_model` = `claude-opus-4-7` (stronger judge)

Every change to the auditor prompt must hold or improve the average score on this dataset before shipping. Same engineering discipline as test suites for code.

## Run

```bash
export ANTHROPIC_API_KEY="your-api-key"
uv pip install anthropic python-dotenv jupyter
jupyter notebook 002_prompting_completed.ipynb   # reference
# or
python -c "from prompt_evaluator import PromptEvaluator; ..."
```
