from dataclasses import dataclass
import time

@dataclass
class Message:
    content: str
    role: str
    timestamp: float = time.time()
