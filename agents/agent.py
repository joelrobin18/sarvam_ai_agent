import json
from typing import Dict
from .llm_client import LLaMAClient
from .tools.crypto_tool import CryptoTool
from .tools.translate_tool import TranslateTool
from models.conversation import Conversation
from models.message import Message
from .exceptions import ToolError

class LLMAgent:
    def __init__(self, llm_api_key: str):
        self.llm = LLaMAClient(llm_api_key)
        self.tools = {'crypto': CryptoTool(), 'translate': TranslateTool()}
        self.conversations: Dict[str, Conversation] = {}

    def _get_or_create_conversation(self, conversation_id: str) -> Conversation:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation(messages=[], context={}, language="en")
        return self.conversations[conversation_id]

    def _should_use_tool(self, llm_response: str) -> dict:
        try:
            tool = json.loads(llm_response)["tool"]
            data = json.loads(llm_response)["data"]
            return {"tool": tool, "data": data}
        except:
            return {}

    def process_message(self, message: str, conversation_id: str) -> str:
        conversation = self._get_or_create_conversation(conversation_id)
        conversation.messages.append(Message(content=message, role="user"))

        try:
            llm_response = self.llm.generate_response(message, conversation.messages)
            tools_data = self._should_use_tool(llm_response)
            if tools_data:
                try:
                    tool_response = self.tools[tools_data['tool'].lower()].execute(tools_data)
                except ToolError as e:
                    tool_response = f"\nTool error: {str(e)}"
                conversation.messages.append(Message(content=llm_response, role="assistant"))
                conversation.messages.append(Message(content=tool_response, role="tool"))
                return tool_response
            else:
                conversation.messages.append(Message(content=llm_response, role="assistant"))
                return llm_response

        except ToolError as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            conversation.messages.append(Message(content=error_message, role="assistant"))
            return error_message
