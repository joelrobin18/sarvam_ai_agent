# Crypto & LLaMA API Client

This project provides a tool for fetching real-time cryptocurrency prices using the CoinGecko API and a language generation client based on LLaMA for generating conversational responses. The CryptoTool handles cryptocurrency price lookups with caching and rate-limiting, while the LLaMAClient processes user prompts for generating contextual responses through the Together API. It also 
has the option to translate sentence based on user query.

## Features

- Real-time cryptocurrency price fetching
- Multi-language support while maintaining English responses
- Conversation context maintenance
- Rate limiting and caching for API calls
- Robust error handling and retry logic
- Secures sensitive information like API keys using .env files.

## Project Structure
```bash
crypto_agent/
├── main.py             
├── models/
│   ├── __init__.py      
│   ├── conversation.py  
│   ├── message.py           
├── agents/
│   ├── tools/
│   │     ├── __init__.py   
│   │     ├──  base_tool.py 
│   │     ├── crypto_tool.py   
│   │     ├── translate_tool.py   
│   ├── agent.py
│   ├── exceptions.py 
│   ├── llm_client.py 
│   ├── prompt_manager.py 
├── .env                     
├── .gitignore
├── README.md
└── requirements.txt         
```

## Getting Started

### Prerequisites
- Python 3.7+
- python-dotenv for environment variable management
- requests, backoff, cachetools

### Installation

1. Clone the repository:
```bash
git clone https://github.com/joelrobin18/sarvam_ai_agent.git
cd crypto_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables. Create a .env file in the root directory to load environment variables.
```bash
export TOGETHER_API_KEY="your-api-key"
```

or
```plaintext
TOGETHER_API_KEY = "your-api-key"
```

4. Load the .env file in your code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")
```

5. To run the agent, follow these steps:
```bash
cd crypto_agent
python3 main.py
```

### Usage

#### Using CryptoTool

- The CryptoTool is designed to fetch cryptocurrency prices with caching and rate-limiting to manage API usage effectively.
- Example Usage:

```python
from crypto_tool import CryptoTool

crypto_tool = CryptoTool()
params = {"data": "bitcoin"}
price_info = crypto_tool.execute(params)
print(price_info)
```

#### Using LLaMAClient
- The LLaMAClient generates responses based on user queries and previous context. Make sure TOGETHER_API_KEY is set in the environment.
- Example Usage:

```python
from crypto_agent import LLMAgent

agent = LLMAgent(llm_api_key="your-api-key")

conversation_id = "user-123"
response = agent.process_message("What's the current Bitcoin price?", conversation_id)
print(response)
```

### Architecture

#### Components

1. **LLMAgent**: Main agent class that orchestrates the conversation flow
2. **LLaMAClient**: Handles communication with the LLaMA 3.1 8B model
3. **Tools**: Modular components for specific tasks
   - CryptoTool: Handles cryptocurrency price queries
   - TranslateTool: Manages language translation requests

#### Prompt Engineering Approach

The system uses a three-part prompt structure:

1. **System Prompt**: Defines the assistant's role, capabilities, and response format.
2. **Conversation History**: Maintains context from the last 10 interactions to provide continuity in the conversation.
3. **Current Query**: The user's latest question or command.

**System Prompt**
- The system prompt sets the rules for interacting with the user and guides tool invocation. 
- It ensures the assistant only calls on available tools, adheres to a JSON format for tool-related responses, and avoids making assumptions when data is unavailable.
- Example System Prompt:

```plaintext
You are a helpful AI assistant specializing in cryptocurrency information and language translation. Your role is to do two things:
1. Answer the questions asked by the user.
2. If you don't have the answer or need external data, call one of the available tools.

Avoid making up answers, and if no tool is available, return:
"No Data and No Tools Available"

For tool invocations, follow this format:
```json
{"tool":"Tool to be invoked", "data":"Input required by the tool"}
When no tool invocation is necessary, simply provide a direct response: "Your response"
```

**Conversation History**
- The conversation history allows continuity across up to 10 previous interactions, helping maintain relevant context.

**User Prompt**
- The user prompt includes the list of available tools and the current conversation context. 
- Here's an example format:

```plaintext
Tools Available: ["Crypto", "Translate"]

Conversations: 
User: What's the price of Bitcoin?
Assistant: {"tool": "Crypto", "data": "bitcoin"}
User: Translate "Hello" to French.
Assistant: {"tool": "Translate", "data": "fr"}
```

### Limitations

- Limited to cryptocurrencies available through the CoinGecko API
- Supports a predefined set of languages for translation
- Maintains only the last 10 messages for context
- Rate limited to 60 API calls per minute
- Caching the data for only 60 seconds

### Future Improvements

1. Add support for more cryptocurrency data sources
2. Implement advanced caching strategies
3. Expand language support
4. Add sentiment analysis for user queries
5. Implement conversation summarization for longer contexts
6. Implement different caching mechanism such as redis

### Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

### License

This project is licensed under the MIT License - see the LICENSE file for details.