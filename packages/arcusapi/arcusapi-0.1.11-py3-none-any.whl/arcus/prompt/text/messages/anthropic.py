from enum import Enum
from typing import Dict, List

import langchain.schema

from arcus.prompt.text.messages.message import BaseMessage, MessageList


class AnthropicRole(Enum):
    ASSISTANT = "assistant"
    USER = "user"


class AnthropicMessage(BaseMessage):
    def __init__(self, message_dict: Dict[str, str]):
        super().__init__(message_dict)

        assert message_dict["role"] in set(
            item.value for item in AnthropicRole
        ), (
            "Invalid Anthropic message: "
            + f"{message_dict}. 'role' must be one of {AnthropicRole}."
        )
        self.role = AnthropicRole(message_dict["role"])

    def get_role(self) -> AnthropicRole:
        return self.role

    def get_langchain_message(self) -> langchain.schema.BaseMessage:
        if self.role == AnthropicRole.ASSISTANT:
            return langchain.schema.AIMessage(content=self.content)
        elif self.role == AnthropicRole.USER:
            return langchain.schema.HumanMessage(content=self.content)
        else:
            raise Exception(f"Invalid Anthropic role: {self.role}.")


class AnthropicMessageList(MessageList):
    def __init__(self, message_list: List[AnthropicMessage]):
        super().__init__(message_list)

    def get_message_list(self) -> List[AnthropicMessage]:
        return self.message_list
