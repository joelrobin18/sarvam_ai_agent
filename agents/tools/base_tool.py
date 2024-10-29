from abc import ABC, abstractmethod
from typing import Dict

class Tool(ABC):
    @abstractmethod
    def execute(self, params: Dict) -> str:
        pass

    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        pass
