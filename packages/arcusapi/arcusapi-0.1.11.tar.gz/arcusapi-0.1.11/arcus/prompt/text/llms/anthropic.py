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

from arcus.api_client import APIClient, ArcusResponse
from arcus.prompt.text.config import Config
from arcus.prompt.text.default_prompts import DEFAULT_CONTEXT_PROMPT
from arcus.prompt.text.llms.llm import LLM, LLMOutput
from arcus.prompt.text.messages import (
    AnthropicMessage,
    AnthropicMessageList,
    AnthropicRole,
)

ANTHROPIC_MODEL_IDS = [
    "claude-instant-1.2",
    "claude-2.0",
]

ANTHROPIC_API_KEY = "ANTHROPIC_API_KEY"


class Anthropic(LLM):
    def __init__(
        self,
        model_id: str,
        config: Config,
        **kwargs,
    ):
        super().__init__(model_id, config)

        assert model_id in ANTHROPIC_MODEL_IDS, (
            "Invalid model_id for Anthropic: "
            + f"{model_id}. Valid model_ids are: {ANTHROPIC_MODEL_IDS}."
        )

        if self.config.get_llm_api_key() is None:
            self.config.set_llm_api_key(
                os.environ.get(ANTHROPIC_API_KEY, None)
            )

        self.model = langchain.chat_models.ChatAnthropic(
            model=model_id,
            anthropic_api_key=self.config.get_llm_api_key(),
            **kwargs,
        )

        self.api_client = APIClient(self.config)

    def _augment_prompt_context(
        self, prompt: str, context_prompt: str = DEFAULT_CONTEXT_PROMPT
    ) -> Tuple[str, str]:
        response: ArcusResponse = self.api_client.request(
            "POST",
            "/prompt/enrich",
            {
                "project_id": self.config.get_project_id(),
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

    def _construct_llm_call(
        self, prompt_messages: AnthropicMessageList
    ) -> str:
        return self.model(
            [
                message.get_langchain_message()
                for message in prompt_messages.get_message_list()
            ]
        ).content

    def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        context_prompt: str = DEFAULT_CONTEXT_PROMPT,
    ) -> LLMOutput:
        if not isinstance(prompt, str):
            prompt_messages = AnthropicMessageList(
                [AnthropicMessage(message_dict) for message_dict in prompt]
            )
        else:
            prompt_messages = AnthropicMessageList(
                [
                    AnthropicMessage(
                        {
                            "role": AnthropicRole.USER.value,
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
