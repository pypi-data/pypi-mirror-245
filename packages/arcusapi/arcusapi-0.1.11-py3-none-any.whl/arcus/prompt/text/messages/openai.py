# Copyright [2023] [Arcus Inc.]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from enum import Enum
from typing import Dict, List

import langchain.schema

from arcus.prompt.text.messages.message import BaseMessage, MessageList


class OpenAIRole(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"


class OpenAIMessage(BaseMessage):
    def __init__(self, message_dict: Dict[str, str]):
        super().__init__(message_dict)

        assert message_dict["role"] in set(
            item.value for item in OpenAIRole
        ), (
            "Invalid OpenAI message: "
            + f"{message_dict}. 'role' must be one of {OpenAIRole}."
        )
        self.role = OpenAIRole(message_dict["role"])

    def get_role(self) -> OpenAIRole:
        return self.role

    def get_langchain_message(self) -> langchain.schema.BaseMessage:
        if self.role == OpenAIRole.SYSTEM:
            return langchain.schema.SystemMessage(content=self.content)
        elif self.role == OpenAIRole.ASSISTANT:
            return langchain.schema.AIMessage(content=self.content)
        elif self.role == OpenAIRole.USER:
            return langchain.schema.HumanMessage(content=self.content)
        else:
            raise Exception(f"Invalid OpenAI role: {self.role}.")


class OpenAIMessageList(MessageList):
    def __init__(self, message_list: List[OpenAIMessage]):
        super().__init__(message_list)

    def get_message_list(self) -> List[OpenAIMessage]:
        return self.message_list
