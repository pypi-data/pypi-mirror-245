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


from abc import ABC, abstractmethod
from typing import Dict, List


class Message(ABC):
    @abstractmethod
    def get_message_dict(self) -> Dict:
        pass

    @abstractmethod
    def get_content(self) -> str:
        pass

    @abstractmethod
    def set_content(self, content: str) -> None:
        pass


class BaseMessage(Message):
    def __init__(self, message_dict: Dict[str, str]):
        self.message_dict = message_dict
        message_keys = set(message_dict.keys())

        assert "role" in message_keys, (
            "Invalid message: " + f"{message_dict}. Missing key: 'role'."
        )

        assert "content" in message_keys, (
            "Invalid message: " + f"{message_dict}. Missing key: 'content'."
        )

        self.content = message_dict["content"]
        assert isinstance(self.content, str), (
            "Invalid message: "
            + f"{message_dict}. 'content' must be a string."
        )

    def get_message_dict(self) -> Dict[str, str]:
        return self.message_dict

    def get_content(self) -> str:
        return self.content

    def set_content(self, content: str) -> None:
        self.content = content


class MessageList:
    def __init__(self, message_list: List[Message]):
        self.message_list = message_list

    def get_message_list(self) -> List[Message]:
        return self.message_list

    def get_final_prompt(self) -> str:
        return self.message_list[-1].get_content()

    def set_final_prompt(self, prompt: str) -> None:
        self.message_list[-1].set_content(prompt)
