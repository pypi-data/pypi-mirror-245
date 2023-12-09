from typing import List

from nomos.api_resources.models import (
    OpenAIChatCompletionParams,
)
from nomos.resources.types import (
    TaskLogMetadataWithVariables,
)
from nomos.resources.tasks.providers.base_openai import BaseOpenai
from nomos.resources.logger import Log, NomosLogger
from openai import OpenAI, APIStatusError
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.completion_create_params import Function
from datetime import datetime
import json
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


class Openai(BaseOpenai):
    def __init__(
        self,
        client: OpenAI,
        nomos_logger: NomosLogger,
    ):
        super().__init__(
            client=client,
            nomos_logger=nomos_logger,
        )

    def execute(
        self,
        messages: List[ChatCompletionMessageParam],
        parameters: OpenAIChatCompletionParams,
        log_metadata: TaskLogMetadataWithVariables,
    ) -> ChatCompletion:
        chat_completion_args = dict(
            messages=messages,
        )
        for key, value in parameters.to_dict().items():
            if key not in set(
                [
                    "model",
                    "top_p",
                    "temperature",
                    "stop",
                    "max_tokens",
                    "presence_penalty",
                    "frequency_penalty",
                    "logit_bias",
                    "function_call",
                    "functions",
                    "user",
                ]
            ):
                continue
            # Convert functions into openai's format
            if key == "functions":
                openai_functions: List[Function] = []
                for nomos_function in value:
                    try:
                        function_parameters = (
                            json.loads(nomos_function["parameters"]["value"])
                            if nomos_function["parameters"]["type"] == "dynamic"
                            else nomos_function["parameters"]["value"]
                        )
                    except Exception:
                        raise ValueError(
                            f'Unable to parse function parameters value as json {nomos_function["parameters"]["value"]}'
                        )
                    openai_functions.append(
                        Function(
                            **{
                                k: v
                                for k, v in nomos_function.items()
                                if k != "parameters"
                            },
                            parameters=function_parameters,
                        )
                    )
                chat_completion_args[key] = openai_functions
            else:
                chat_completion_args[key] = value

        start_time = datetime.utcnow()
        try:
            chat_completion: ChatCompletion = self.client.chat.completions.create(
                **chat_completion_args,
            )
        except APIStatusError as e:
            self.nomos_logger.safe_log(
                log=Log(
                    provider=parameters.provider_name,
                    model=parameters.model,
                    request_path=parameters.provider_function,
                    request_body=chat_completion_args,
                    response_status=e.status_code,
                    request_start_time=start_time,
                    request_end_time=datetime.utcnow(),
                    response=e.response.json(),
                    **log_metadata,
                )
            )
            raise e

        self.nomos_logger.safe_log(
            log=Log(
                provider=parameters.provider_name,
                model=parameters.model,
                request_path=parameters.provider_function,
                request_body=chat_completion_args,
                response_status=200,
                request_start_time=start_time,
                request_end_time=datetime.utcnow(),
                response=chat_completion.model_dump(exclude_unset=True),
                **log_metadata,
            )
        )

        return chat_completion
