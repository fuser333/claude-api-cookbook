"""PromptEvaluator · class that wraps the eval loop from the course.

Workflow:
    1. generate_dataset(task_description, prompt_inputs_spec, num_cases) → dataset.json
    2. run_evaluation(prompt_template, dataset_file) → results with model+syntax grading
    3. summary() → aggregated pass rate per version
"""
import os
import json
import asyncio
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class PromptEvaluator:
    def __init__(self, max_concurrent_tasks: int = 2, generator_model: str = "claude-haiku-4-5",
                 grader_model: str = "claude-sonnet-4-5"):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.generator_model = generator_model   # Haiku · barato, volumen
        self.grader_model = grader_model         # Sonnet · juicio sólido
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    # ------------------------------------------------------------------ #
    # Stage 1: generate dataset
    # ------------------------------------------------------------------ #
    def generate_dataset(self, task_description: str, prompt_inputs_spec: dict,
                         output_file: str = "dataset.json", num_cases: int = 4) -> list:
        """Synthesize test cases that exercise the prompt under test."""
        spec_text = json.dumps(prompt_inputs_spec, indent=2)
        gen_prompt = f"""
You are generating a synthetic evaluation dataset for the following prompt:

TASK: {task_description}

INPUT SPEC (each test case must include keys with realistic values for these):
{spec_text}

Generate exactly {num_cases} diverse test cases as a JSON array. Each case must be
realistic, varied in style and topic, and cover edge conditions when possible.
Output ONLY the JSON array · no preamble · no commentary.
""".strip()

        resp = client.messages.create(
            model=self.generator_model,
            max_tokens=4000,
            messages=[{"role": "user", "content": gen_prompt}],
        )
        text = resp.content[0].text.strip()
        # Strip code fences if any
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        dataset = json.loads(text)
        with open(output_file, "w") as f:
            json.dump(dataset, f, indent=2)
        return dataset

    # ------------------------------------------------------------------ #
    # Stage 2: run prompt under test against each case
    # ------------------------------------------------------------------ #
    async def _run_one(self, prompt_template: str, case: dict, target_model: str) -> dict:
        async with self.semaphore:
            filled = prompt_template.format(**case)
            resp = await asyncio.to_thread(
                client.messages.create,
                model=target_model,
                max_tokens=2048,
                messages=[{"role": "user", "content": filled}],
            )
            return {"input": case, "output": resp.content[0].text}

    async def _run_all(self, prompt_template: str, dataset: list, target_model: str) -> list:
        return await asyncio.gather(*[self._run_one(prompt_template, c, target_model)
                                       for c in dataset])

    # ------------------------------------------------------------------ #
    # Stage 3: grade each output (model + deterministic)
    # ------------------------------------------------------------------ #
    def grade_by_model(self, task_description: str, case_input: dict, output: str) -> dict:
        rubric_prompt = f"""
You are grading an LLM output. Before the numeric score, list strengths,
weaknesses and reasoning. Then return the score in this exact tag:
<score>0.0 to 1.0</score>

TASK: {task_description}
INPUT: {json.dumps(case_input, indent=2)}
OUTPUT: {output}
""".strip()

        resp = client.messages.create(
            model=self.grader_model,
            max_tokens=1024,
            messages=[{"role": "user", "content": rubric_prompt}],
        )
        text = resp.content[0].text
        import re
        m = re.search(r"<score>([\d.]+)</score>", text)
        score = float(m.group(1)) if m else 0.0
        return {"score": score, "rationale": text}

    @staticmethod
    def validate_json(text: str) -> bool:
        try:
            json.loads(text)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    # Convenience entry point
    # ------------------------------------------------------------------ #
    def run_evaluation(self, task_description: str, prompt_template: str,
                       dataset: list, target_model: str = "claude-sonnet-4-5") -> dict:
        outputs = asyncio.run(self._run_all(prompt_template, dataset, target_model))
        graded = []
        for r in outputs:
            grade = self.grade_by_model(task_description, r["input"], r["output"])
            graded.append({
                **r,
                "model_score": grade["score"],
                "json_valid": self.validate_json(r["output"]),
            })
        avg = sum(g["model_score"] for g in graded) / len(graded) if graded else 0.0
        return {"results": graded, "average_score": avg,
                "json_pass_rate": sum(g["json_valid"] for g in graded) / len(graded)}
