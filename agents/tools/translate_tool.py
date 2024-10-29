from .base_tool import Tool
from typing import Dict

# TODO this can be changed according to our use case such as translation etc
class TranslateTool(Tool):
    def __init__(self):
        self.supported_languages = {
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ml': 'Malayalam'
        }

    def execute(self, params: Dict) -> str:
        target_lang = params.get('data', '').lower()
        if target_lang not in self.supported_languages:
            raise Exception(f"Unsupported language: {target_lang}")
        return f"Language changed to {self.supported_languages[target_lang]}"

    def can_handle(self, intent: str) -> bool:
        return "translate" in intent.lower() or "language" in intent.lower()
