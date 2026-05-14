# Prompt Evaluations · Lab notebooks

Two-stage prompt evaluation workflow from the Anthropic Academy course "Building with the Claude API".

## Files

| Notebook | Stage | Purpose |
|----------|-------|---------|
| `001_prompt_evals.ipynb` | Generation | Defines helpers + `generate_dataset()` that synthesizes a dataset of Python / JSON / Regex AWS-related tasks |
| `001_prompt_evals_grader.ipynb` | Model-graded eval | Adds `grade_by_model()`, `run_prompt()`, `run_test_case()`, `run_eval()` to score outputs systematically using another Claude as judge |
| `001_prompt_evals_fns.ipynb` | Deterministic validators | Adds `validate_json()`, `validate_python()`, `validate_regex()` to fail-fast on outputs that don't even parse / compile |

## The evaluation pattern (the most underrated skill in this course)

1. **Generate dataset** — synthesize 10-100 input cases that cover the prompt's intended use
2. **Run prompt** — execute the prompt under test against each dataset entry
3. **Grade by model** — a separate Claude call scores each output against a rubric (correctness, format, completeness)
4. **Aggregate** — compute pass rate / average score · compare prompt versions side-by-side
5. **Iterate** — change one variable at a time (system prompt, temperature, model, structure)

## Why this matters

Without evaluations, "prompt engineering" is folklore. The grader notebook formalizes the loop:

```
prompt_version → run on dataset → model grades outputs → score → improve → re-run
```

This is the same workflow Anthropic uses internally to ship prompts. Production-grade Claude integrations always include an eval suite.

## Production application at H3L Consulting

We use this pattern in the H3L Diagnostics platform to evaluate the auditor prompts that classify "capacidad atrapada" categories across 332,460 Ecuadorian companies. Each prompt version gets a regression test against a frozen golden dataset before it ships to production.

## Run

```bash
export ANTHROPIC_API_KEY="your-api-key"
uv pip install anthropic python-dotenv jupyter
jupyter notebook 001_prompt_evals.ipynb
# then 001_prompt_evals_grader.ipynb
```
