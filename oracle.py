# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class SimpleOracle(gl.Contract):
    question: str
    answer: str

    def __init__(self, initial_question: str):
        self.question = initial_question
        self.answer = ""

    @gl.public.view
    def get_answer(self) -> str:
        return self.answer

    @gl.public.write
    def ask(self, new_question: str) -> None:
        self.question = new_question

        prompt = f"""
Answer the question briefly.
Respond ONLY in this JSON format:
{{"answer": str}}

Question: {new_question}
"""

        def get_answer():
            result = gl.nondet.exec_prompt(prompt)
            return result.replace("```json", "").replace("```", "")

        result = gl.eq_principle.prompt_comparative(
            get_answer,
            "The value of answer must match"
        )

        parsed = json.loads(result)
        self.answer = parsed["answer"]
