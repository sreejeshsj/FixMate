import requests
import re

class LLMClient:
    def __init__(self, model_name: str = "deepseek-r1-distill-llama-70b"):
        self.model_name = model_name
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        # ✅ Hardcoded API Key (unchanged)
        self.api_key = "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"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, code: str, objective: str = "") -> str:
        """
        Fixes syntax and logical errors in code.
        Accepts an optional objective string describing what the code is supposed to do.
        Returns ONLY the corrected code.
        """
        instruction = "Fix errors in the following code."
        if objective:
            instruction += f" The code is intended to: {objective}."
        instruction += (
            " Return ONLY the corrected code as raw text with NO explanations, markdown, or comments."
            " If there is no error, return the original code."
        )

        prompt = f"{instruction}\n\n{code}"

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 20000
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            output_text = response.json()["choices"][0]["message"]["content"].strip()

            # ✅ Remove markdown code blocks if present
            match = re.search(r"```(?:python)?\n?(.*?)```", output_text, re.DOTALL)
            if match:
                return match.group(1).strip()

            # ✅ Filter unnecessary comments or text
            lines = output_text.split("\n")
            filtered_lines = [line for line in lines if not line.strip().startswith("#") and line.strip()]
            return "\n".join(filtered_lines)

        else:
            return f"Error: {response.status_code} - {response.text}"
