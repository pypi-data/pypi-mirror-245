from abc import ABC, abstractmethod
from typing import List, Set, Union

from nomos.resources.logger import NomosLogger

from nomos.api_resources.models import (
    AzureOpenAIChatCompletionParams,
    OpenAIChatCompletionParams,
    AzureOpenAIChatCompletionPrompt,
    OpenAIChatCompletionPrompt,
    OpenAIFunctionCallObject,
    OpenAIFunction,
    DynamicParameters,
    OpenAIChatCompletionParamsFunctionCall,
)
from nomos.resources.types import (
    TaskLogMetadata,
    FunctionResponse,
    TaskLogMetadataWithVariables,
    ExecuteResult,
)
from nomos.resources.variable_parser import VariablesData, VariableParser
from nomos.resources.prompt_parser import PromptParser
from openai import OpenAI, AzureOpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


class BaseOpenai(ABC):
    def __init__(
        self,
        client: Union[OpenAI, AzureOpenAI],
        nomos_logger: NomosLogger,
    ):
        self.client = client
        self.nomos_logger = nomos_logger

    def execute_prompt(
        self,
        prompt: Union[OpenAIChatCompletionPrompt, AzureOpenAIChatCompletionPrompt],
        parameters: Union[OpenAIChatCompletionParams, AzureOpenAIChatCompletionParams],
        chat_history: List[ChatCompletionMessageParam],
        variables: VariablesData,
        log_metadata: TaskLogMetadata,
    ) -> ExecuteResult:
        parsed_prompt = PromptParser.get_parsed_prompt(
            prompt=prompt,
            variables=variables,
        )

        # Copy chat history to avoid modifying the original
        messages = chat_history[:]

        for _, message in enumerate(parsed_prompt.messages):
            messages.append(message.to_dict())

        completion: ChatCompletion = self.execute(
            messages,
            parameters,
            log_metadata=TaskLogMetadataWithVariables(
                **log_metadata,
                variables=variables,
            ),
        )
        return ExecuteResult(
            history=messages
            + [
                choice.message.model_dump(exclude_unset=True)
                for choice in completion.choices
            ],
            data=completion,
        )

    def send_function_response(
        self,
        parameters: Union[OpenAIChatCompletionParams, AzureOpenAIChatCompletionParams],
        chat_history: List[ChatCompletionMessageParam],
        function_response: FunctionResponse,
        log_metadata: TaskLogMetadataWithVariables,
    ) -> ExecuteResult:
        messages = chat_history[:]
        messages.append(
            {
                "role": "function",
                "name": function_response["name"],
                "content": function_response["response"],
            }
        )
        completion: ChatCompletion = self.execute(
            messages,
            parameters,
            log_metadata,
        )
        return ExecuteResult(
            history=messages
            + [
                choice.message.model_dump(exclude_unset=True)
                for choice in completion.choices
            ],
            data=completion,
        )

    def parse_parameters(
        self,
        parameters: Union[AzureOpenAIChatCompletionParams, OpenAIChatCompletionParams],
        variables: VariablesData,
    ) -> Union[AzureOpenAIChatCompletionParams, OpenAIChatCompletionParams]:
        if not isinstance(
            parameters, (AzureOpenAIChatCompletionParams, OpenAIChatCompletionParams)
        ):
            raise ValueError(f"Parameters {parameters} is not supported")
        new_parameters = dict()
        if parameters.function_call is not None and isinstance(
            parameters.function_call.actual_instance, OpenAIFunctionCallObject
        ):
            name = VariableParser.populate_variables(
                content=parameters.function_call.actual_instance.name,
                variables=variables,
            )
            new_parameters["function_call"] = OpenAIChatCompletionParamsFunctionCall(
                OpenAIFunctionCallObject(
                    name=name,
                )
            )

        if parameters.functions is not None:
            new_functions_value: List[OpenAIFunction] = []
            for function in parameters.functions:
                new_function_args = dict()
                if function.description is not None:
                    new_function_args[
                        "description"
                    ] = VariableParser.populate_variables(
                        content=function.description,
                        variables=variables,
                    )
                new_function_args["name"] = VariableParser.populate_variables(
                    content=function.name,
                    variables=variables,
                )

                new_function_args[
                    "parameters"
                ] = function.parameters.actual_instance.model_dump()
                if isinstance(function.parameters.actual_instance, DynamicParameters):
                    new_function_args["parameters"] = dict(
                        type=function.parameters.actual_instance.type,
                        value=VariableParser.populate_variables(
                            content=function.parameters.actual_instance.value,
                            variables=variables,
                        ),
                    )
                new_functions_value.append(OpenAIFunction.from_dict(new_function_args))
            new_parameters["functions"] = new_functions_value
        # TODO: model_copy console.warns serialization issues. Look into alternatives
        return parameters.model_copy(update=new_parameters)

    def get_parameter_variables(
        self,
        parameters: Union[AzureOpenAIChatCompletionParams, OpenAIChatCompletionParams],
    ) -> Set[str]:
        variables = set()
        if parameters.functions is not None:
            for function in parameters.functions:
                variables.update(VariableParser.find_variables(function.name))
                if function.description is not None:
                    variables.update(
                        VariableParser.find_variables(function.description)
                    )
                if isinstance(function.parameters.actual_instance, DynamicParameters):
                    variables.update(
                        VariableParser.find_variables(
                            function.parameters.actual_instance.value
                        )
                    )
        if parameters.function_call is not None and isinstance(
            parameters.function_call.actual_instance, OpenAIFunctionCallObject
        ):
            variables.update(
                VariableParser.find_variables(
                    parameters.function_call.actual_instance.name
                )
            )
        return variables

    @abstractmethod
    def execute(
        self,
        log_metadata: TaskLogMetadataWithVariables,
        *args,
        **kwargs,
    ) -> ChatCompletion:
        pass
