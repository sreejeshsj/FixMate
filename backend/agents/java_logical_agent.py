from typing import List, Tuple
from ..models.errors import CodeError  # Assuming CodeError class exists

class JavaLogicalAgent:
    def __init__(self, llm_client):
        self.llm = llm_client  # Use the provided LLM client

    def fix_logical_errors(self, java_code: str, objective: str) -> Tuple[str, List[CodeError]]:
        """Fix logical errors in Java code using LLM with an objective."""
        errors = []

        try:
            # Send both java_code and objective to the LLM
            prompt = f"Fix logical errors in the following Java code:\n{java_code}\nObjective: {objective}"
            corrected_code = self.llm.generate(java_code, objective)  # Sends both code and objective

            if corrected_code.strip() != java_code.strip():
                errors.append(CodeError(
                    error_type="logical",
                    message="Possible logical issues found and fixed."
                ))

        except Exception as e:
            errors.append(CodeError(
                error_type="logical",
                message=f"Error during logical analysis: {str(e)}"
            ))
            return java_code, errors

        return corrected_code, errors
