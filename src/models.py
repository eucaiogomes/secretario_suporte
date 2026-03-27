from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    path: str
    filename: str
    content: str
    score: float = 0.0
