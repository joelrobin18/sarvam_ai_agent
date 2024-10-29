from .base_tool import Tool
from cachetools import TTLCache
import requests
import time
import logging
import backoff
from typing import Dict
from ..exceptions import ToolError

# Logging Configuration
logger = logging.getLogger(__name__)

class CryptoTool:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=60)  
        self.api_calls = []
        self.rate_limit = 60

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
    def execute(self, params: Dict) -> str:
        symbol = params.get('data', 'bitcoin')

        # Check cache first
        cache_key = f"price_{symbol}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Rate limiting check
        current_time = time.time()
        self.api_calls = [t for t in self.api_calls if current_time - t < 60]
        if len(self.api_calls) >= self.rate_limit:
            raise ToolError("Rate limit exceeded for Crypto API")

        try:
            response = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price",
                params={"ids": symbol.lower(), "vs_currencies": "usd"},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            if not data or symbol.lower() not in data:
                raise ToolError(f"No data found for {symbol}")

            result = f"Current price of {symbol}: ${data[symbol.lower()]['usd']:,.2f}"
            self.cache[cache_key] = result 
            self.api_calls.append(current_time) 
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise ToolError(f"Failed to fetch price for {symbol}")

    def can_handle(self, intent: str) -> bool:
        return "price" in intent.lower() or "bitcoin" in intent.lower() or "crypto" in intent.lower()