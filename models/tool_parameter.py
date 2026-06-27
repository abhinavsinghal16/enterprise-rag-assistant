from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolParameter:
    """
    Describes a single input parameter expected by a tool.
    """

    name: str
    type: type
    description: str
    required: bool = True
    default: Any = None
