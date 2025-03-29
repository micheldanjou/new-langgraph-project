"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class State:
    """Defines the input state for the agent.
    
    This class is used to define the initial state and structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    for more information.
    """
    
    messages: List[Dict[str, Any]] = field(default_factory=list)
    current_message: str = ""
