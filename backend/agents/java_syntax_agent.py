from typing import List, Tuple
from ..models.errors import CodeError  # Assuming CodeError is defined in models/errors

class JavaSyntaxAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def detect_syntax_errors(self, java_code: str) -> List[CodeError]:
        """
        Uses LLM to detect syntax errors in Java code.
        """
        prompt = f"Analyze the following Java code and list any syntax errors with line numbers:\n\n{java_code}"
        response = self.llm_client.generate(prompt)

        errors = []
        for line in response.split("\n"):
            if "line" in line.lower():
                parts = line.split(":")
                if len(parts) >= 2:
                    try:
                        line_number = int(parts[0].strip().split()[-1])
                        message = ":".join(parts[1:]).strip()
                        errors.append(CodeError(
                            error_type="syntax",
                            message=message,
                            line_number=line_number
                        ))
                    except ValueError:
                        continue
        return errors

    def fix_syntax_errors(self, java_code: str, objective: str) -> Tuple[str, List[CodeError]]:
        """
        Uses LLM to detect and fix syntax errors in Java code.
        """
        errors = self.detect_syntax_errors(java_code)

        if not errors:
            return java_code, []

        prompt = f"Fix the syntax errors in the following Java code:\n\n{java_code}\n\nObjective: {objective}"
        corrected_code = self.llm_client.generate(prompt)

        return corrected_code, errors
