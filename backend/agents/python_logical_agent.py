import ast
from typing import List, Tuple
from ..models.errors import CodeError

class PythonLogicalAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def fix_logical_errors(self, code: str, objective: str) -> Tuple[str, List[CodeError]]:
        errors = []

        try:
            corrected_code = self.llm_client.generate(code, objective)

            if corrected_code.strip() != code.strip():
                errors.append(CodeError(
                    error_type='logical',
                    message='Possible logical issues found and fixed.'
                ))

        except Exception as e:
            errors.append(CodeError(
                error_type='logical',
                message=f"Error during logical analysis: {str(e)}"
            ))
            return code, errors  # Return original code on failure

        return corrected_code, errors
