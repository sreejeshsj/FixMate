#core.py
from typing import Tuple, List
from .agents.python_syntax_agent import PythonSyntaxAgent
from .agents.python_logical_agent import PythonLogicalAgent
from .agents.java_syntax_agent import JavaSyntaxAgent
from .agents.java_logical_agent import JavaLogicalAgent
from .models.errors import CodeError

class LanguageIdentificationAgent:
    def identify_language(self, code: str) -> str:
        """Detect if the given code is Python or Java."""
        if "public class" in code or "System.out.println" in code:
            return "java"
        elif "def " in code or "print(" in code:
            return "python"
        return "unknown"

class FixMate:
    def __init__(self, llm_client):
        self.lang_identifier = LanguageIdentificationAgent()
        # Python Agents
        self.python_syntax_agent = PythonSyntaxAgent(llm_client)
        self.python_logical_agent = PythonLogicalAgent(llm_client)
        # Java Agents
        self.java_syntax_agent = JavaSyntaxAgent(llm_client)
        self.java_logical_agent = JavaLogicalAgent(llm_client)

    def repair_code(self, code: str, objective: str) -> Tuple[str, List[CodeError]]:
        all_errors = []
        lang = self.lang_identifier.identify_language(code)

        if lang == "python":
            syntax_agent = self.python_syntax_agent
            logical_agent = self.python_logical_agent
        elif lang == "java":
            syntax_agent = self.java_syntax_agent
            logical_agent = self.java_logical_agent
        else:
            return "Error: Unknown language detected.", []

        # Fix syntax errors first
        code, syntax_errors = syntax_agent.fix_syntax_errors(code, objective)
        all_errors.extend(syntax_errors)
        
        # Then fix logical errors if no syntax errors remain
        if not syntax_errors:
            print("1")
            code, logical_errors = logical_agent.fix_logical_errors(code, objective)
            all_errors.extend(logical_errors)
        print(all_errors)
        if not all_errors:
            return code, [CodeError(message="No errors detected. Code is correct.", line_number=0, fix_applied=False)]
         
        return code, all_errors
