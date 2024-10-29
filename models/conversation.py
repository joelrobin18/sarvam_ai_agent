from dataclasses import dataclass
from typing import Dict, List
from .message import Message

@dataclass
class Conversation:
    messages: List[Message]
    context: Dict
    language: str = "en"
