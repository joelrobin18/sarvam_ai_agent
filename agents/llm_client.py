import requests
import backoff
import logging
from typing import List, Dict
from .exceptions import AgentError
from models.conversation import Conversation
from models.message import Message
from .prompt_manager import PromptManager
import time

# Logging Configuration
logger = logging.getLogger(__name__)

class LLaMAClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.prompt_manager = PromptManager()

        self.cache: Dict[str, str] = {}
        self.api_calls: List[float] = [] 
        self.rate_limit = 60  
        self.time_window = 60

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
    def generate_response(self, prompt: str, context: List[Message]) -> str:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        user_prompt = self.prompt_manager.create_user_prompt(context)

        # Caching
        if user_prompt in self.cache:
            return self.cache[user_prompt]
        
        # Rate limiting
        current_time = time.time()
        self.api_calls = [t for t in self.api_calls if current_time - t < self.time_window]
        if len(self.api_calls) >= self.rate_limit:
            logger.error("Rate limit exceeded.")
            raise AgentError("Rate limit exceeded. Try again later.")

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json={
                    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                    "messages": [
                        {"role": "system", "content": self.prompt_manager.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content']
            
            # Store response in cache
            self.cache[user_prompt] = result
            self.api_calls.append(current_time)  
            return result
        except Exception as e:
            logger.error(f"LLM API error: {str(e)}")
            raise AgentError("Failed to generate response")