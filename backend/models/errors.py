from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeError:
    error_type: str
    message: str
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None