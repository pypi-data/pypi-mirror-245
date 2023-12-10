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


import os
from typing import Dict, List, Tuple, Union

import langchain.chat_models
import langchain.llms

from arcus.api_client import APIClient, ArcusResponse
from arcus.prompt.text.config import Config
from arcus.prompt.text.default_prompts import DEFAULT_CONTEXT_PROMPT
from arcus.prompt.text.llms.llm import LLM, LLMOutput
from arcus.prompt.text.messages import (
    CohereMessage,
    CohereMessageList,
    CohereRole,
)

COHERE_MODEL_IDS = [
    "command",
    "command-light",
]

COHERE_MAX_TOKENS = {
    "command": 4096,
    "command-light": 4096,
}

HELPFUL_ASSISTANT_SYSTEM_MESSAGE = CohereMessage(
    {
        "role": CohereRole.SYSTEM.value,
        "content": "You are a helpful assistant.",
    }
)

COHERE_API_KEY = "COHERE_API_KEY"


class Cohere(LLM):
    def __init__(
        self,
        model_id: str,
        config: Config,
        # both command and command-light are used interchangeably as chat model
        # and llms, so the user needs to specify if they are using a chat model
        is_chat: bool = True,
        **kwargs,
    ):
        super().__init__(model_id, config)

        assert model_id in COHERE_MODEL_IDS, (
            "Invalid model_id for Cohere: "
            + f"{model_id}. Valid model_ids are: {COHERE_MODEL_IDS}."
        )

        self._is_chat = is_chat

        if self.config.get_llm_api_key() is None:
            self.config.set_llm_api_key(os.environ.get(COHERE_API_KEY, None))

        if self.is_chat():
            self.model = langchain.chat_models.ChatCohere(
                model=model_id,
                cohere_api_key=self.config.get_llm_api_key(),
                **kwargs,
            )
        else:
            self.model = langchain.llms.Cohere(
                model=model_id,
                cohere_api_key=self.config.get_llm_api_key(),
                **kwargs,
            )

        self.api_client = APIClient(self.config)

    def _get_max_tokens_remaining(self, prompt: str) -> int:
        return COHERE_MAX_TOKENS[self.model_id] - self.model.get_num_tokens(
            prompt
        )

    def _augment_prompt_context(
        self, prompt: str, context_prompt: str = DEFAULT_CONTEXT_PROMPT
    ) -> Tuple[str, str]:
        if not self.is_chat():
            max_tokens_remaining = self._get_max_tokens_remaining(prompt)
        else:
            max_tokens_remaining = None

        response: ArcusResponse = self.api_client.request(
            "POST",
            "/prompt/enrich",
            {
                "project_id": self.config.get_project_id(),
                "max_tokens_remaining": max_tokens_remaining,
            },
            json={
                "prompt": prompt,
                "context_prompt": context_prompt,
            },
        )

        if not response.status_ok:
            raise Warning(
                f"Failed to get additional context for prompt: {prompt}. "
                + f"Response: {response}"
            )
            return prompt, ""

        enriched_prompt = response.data["enriched_prompt"]
        context_summary = response.data["context_summary"]

        return enriched_prompt, context_summary

    def _construct_llm_call(self, prompt_messages: CohereMessageList) -> str:
        if self.is_chat():
            # langchain ChatCohere model takes the first element of the list
            # as the message and the rest of the list as the chat history
            message_list = prompt_messages.get_message_list()
            chat_history = message_list[:-1]
            message = message_list[-1]
            chat_list = [message] + chat_history
            return self.model(
                [message.get_langchain_message() for message in chat_list]
            ).content

        return self.model(prompt_messages.get_final_prompt())

    def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        context_prompt: str = DEFAULT_CONTEXT_PROMPT,
    ) -> LLMOutput:
        if not isinstance(prompt, str):
            prompt_messages = CohereMessageList(
                [CohereMessage(message_dict) for message_dict in prompt]
            )
        else:
            prompt_messages = CohereMessageList(
                [
                    HELPFUL_ASSISTANT_SYSTEM_MESSAGE,
                    CohereMessage(
                        {
                            "role": CohereRole.USER.value,
                            "content": prompt,
                        }
                    ),
                ]
            )

        enriched_prompt, context_summary = self._augment_prompt_context(
            prompt_messages.get_final_prompt(), context_prompt
        )

        prompt_messages.set_final_prompt(enriched_prompt)

        return LLMOutput(
            self._construct_llm_call(prompt_messages), context_summary
        )

    def is_chat(self) -> bool:
        return self._is_chat
