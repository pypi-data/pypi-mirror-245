from typing import TYPE_CHECKING, List
from openai import APIStatusError
from openai.types.chat.completion_create_params import CompletionCreateParamsBase
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChatCompletion
from nomos.api_resources.models.provider_function import ProviderFunction
from nomos.api_resources.models.provider_name import ProviderName
from nomos.resources.logger import Log, NomosLogger

from nomos.resources.types import ExecuteResult, LogMetadata
from datetime import datetime

# Avoids circular import issues with typing
if TYPE_CHECKING:
    from ..client import Nomos


class OpenaiMessage:
    def __init__(
        self, parameters: CompletionCreateParamsBase, nomos_logger: NomosLogger
    ):
        self.parameters = parameters
        self.nomos_logger = nomos_logger

    def execute(
        self,
        client: "Nomos",
        history: List[ChatCompletionMessageParam],
        log_metadata: LogMetadata,
    ) -> ExecuteResult:
        parameters = dict(self.parameters)
        parameters["messages"] = history + self.parameters["messages"]

        start_time = datetime.utcnow()
        try:
            completion: ChatCompletion = client.openai_client.chat.completions.create(
                **parameters,
            )
        except APIStatusError as e:
            self.nomos_logger.safe_log(
                log=Log(
                    provider=ProviderName.OPENAI,
                    model=parameters["model"],
                    request_path=ProviderFunction.CHAT_COMPLETION,
                    request_body=parameters,
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
                provider=ProviderName.OPENAI,
                model=parameters["model"],
                request_path=ProviderFunction.CHAT_COMPLETION,
                request_body=parameters,
                response_status=200,
                request_start_time=start_time,
                request_end_time=datetime.utcnow(),
                response=completion.model_dump(exclude_unset=True),
                **log_metadata,
            )
        )

        new_history = list(parameters["messages"])
        for choice in completion.choices:
            new_history.append(choice.message.model_dump(exclude_unset=True))
        return ExecuteResult(
            history=new_history,
            data=completion,
        )
