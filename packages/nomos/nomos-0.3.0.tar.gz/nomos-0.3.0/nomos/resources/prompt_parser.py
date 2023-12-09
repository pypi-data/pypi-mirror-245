from typing import Set, Union
from nomos.api_resources.models import (
    OpenAIChatCompletionPrompt,
    OpenAICompletionPrompt,
    AzureOpenAIChatCompletionPrompt,
)
from nomos.resources.variable_parser import (
    VariablesData,
    VariableParser,
)


class PromptParser:
    @classmethod
    def get_parsed_prompt(
        cls,
        prompt: Union[
            OpenAIChatCompletionPrompt,
            OpenAICompletionPrompt,
            AzureOpenAIChatCompletionPrompt,
        ],
        variables: VariablesData,
    ) -> Union[
        OpenAIChatCompletionPrompt,
        OpenAICompletionPrompt,
        AzureOpenAIChatCompletionPrompt,
    ]:
        if isinstance(prompt, OpenAIChatCompletionPrompt) or isinstance(
            prompt, AzureOpenAIChatCompletionPrompt
        ):
            return cls._parse_chat_completion_prompt(prompt, variables)
        elif isinstance(prompt, OpenAICompletionPrompt):
            return cls._parse_completion_prompt(prompt, variables)
        else:
            raise ValueError(f"Unsupported prompt type: {type(prompt)}")

    @classmethod
    def get_variables(
        cls,
        prompt: Union[
            OpenAIChatCompletionPrompt,
            AzureOpenAIChatCompletionPrompt,
            OpenAICompletionPrompt,
        ],
    ) -> Set[str]:
        if isinstance(
            prompt, (OpenAIChatCompletionPrompt, AzureOpenAIChatCompletionPrompt)
        ):
            variables = set()
            for message in prompt.messages:
                if message.content is not None:
                    variables.update(VariableParser.find_variables(message.content))
            return variables
        elif isinstance(prompt, OpenAICompletionPrompt):
            return set(VariableParser.find_variables(prompt.content))
        else:
            raise ValueError(f"Unsupported prompt type: {type(prompt)}")

    @classmethod
    def _parse_chat_completion_prompt(
        cls,
        prompt: Union[
            OpenAIChatCompletionPrompt,
            AzureOpenAIChatCompletionPrompt,
        ],
        variables: VariablesData,
    ) -> Union[OpenAIChatCompletionPrompt, AzureOpenAIChatCompletionPrompt]:
        new_messages = []
        for _, message in enumerate(prompt.messages):
            new_message = dict(role=message.role)
            if message.content is not None:
                content = VariableParser.populate_variables(
                    content=message.content,
                    variables=variables,
                )
                new_message["content"] = content
            for key, value in message.to_dict().items():
                if key == "content":
                    continue
                new_message[key] = value
            new_messages.append(new_message)
        return prompt.__class__(
            messages=new_messages,
            provider_name=prompt.provider_name,
            provider_function=prompt.provider_function,
        )

    @classmethod
    def _parse_completion_prompt(
        cls, prompt: OpenAICompletionPrompt, variables: VariablesData
    ) -> OpenAICompletionPrompt:
        content = VariableParser.populate_variables(
            content=prompt.content,
            variables=variables,
        )
        return OpenAICompletionPrompt(
            content=content,
            provider_function=prompt.provider_function,
            provider_name=prompt.provider_name,
        )
