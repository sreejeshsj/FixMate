import ast
from typing import List, Tuple
from ..models.errors import CodeError

class PythonSyntaxAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def check_basic_syntax(self, code: str) -> List[CodeError]:
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(CodeError(
                error_type='syntax',
                message=str(e),
                line_number=e.lineno
            ))
        return errors

    def fix_syntax_errors(self, code: str, objective: str) -> Tuple[str, List[CodeError]]:
        errors = self.check_basic_syntax(code)

        if not errors:
            return code, []

        corrected_code = self.llm_client.generate(code, objective)
        return corrected_code, errors
