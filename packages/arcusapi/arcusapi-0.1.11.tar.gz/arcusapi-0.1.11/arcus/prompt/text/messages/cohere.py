from enum import Enum
from typing import Dict, List

import langchain.schema

from arcus.prompt.text.messages.message import BaseMessage, MessageList


class CohereRole(Enum):
    SYSTEM = "system"
    CHATBOT = "chatbot"
    USER = "user"


class CohereMessage(BaseMessage):
    def __init__(self, message_dict: Dict[str, str]):
        super().__init__(message_dict)

        assert message_dict["role"] in set(
            item.value for item in CohereRole
        ), (
            "Invalid Cohere message: "
            + f"{message_dict}. 'role' must be one of {CohereRole}."
        )
        self.role = CohereRole(message_dict["role"])

    def get_role(self) -> CohereRole:
        return self.role

    def get_langchain_message(self) -> langchain.schema.BaseMessage:
        if self.role == CohereRole.SYSTEM:
            return langchain.schema.SystemMessage(content=self.content)
        elif self.role == CohereRole.CHATBOT:
            return langchain.schema.AIMessage(content=self.content)
        elif self.role == CohereRole.USER:
            return langchain.schema.HumanMessage(content=self.content)
        else:
            raise Exception(f"Invalid Cohere role: {self.role}.")


class CohereMessageList(MessageList):
    def __init__(self, message_list: List[CohereMessage]):
        super().__init__(message_list)

    def get_message_list(self) -> List[CohereMessage]:
        return self.message_list
