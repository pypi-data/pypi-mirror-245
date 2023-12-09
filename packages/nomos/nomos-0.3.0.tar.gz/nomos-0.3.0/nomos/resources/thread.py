from typing import TYPE_CHECKING, List, Optional, Union
from nomos.resources.messages.azure_openai import AzureOpenaiMessage
from nomos.resources.messages.openai import OpenaiMessage
from nomos.resources.project import NomosTask
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from nomos.resources.tasks.task import TaskFunctionResponse
from nomos.resources.types import LogMetadata

from nomos.resources.variable_parser import VariablesData
import uuid

# Avoids circular import issues with typing
if TYPE_CHECKING:
    from .client import Nomos


class NomosThread:
    def __init__(
        self,
        client: "Nomos",
        history: List[ChatCompletionMessageParam],
    ):
        self.client = client
        self.history = history
        self.id = uuid.uuid4()
        self.last_execute_id = None

    def execute(
        self,
        input: Union[
            NomosTask, TaskFunctionResponse, AzureOpenaiMessage, OpenaiMessage
        ],
        variables: Optional[VariablesData] = None,
    ) -> ChatCompletion:
        execute_id = uuid.uuid4()
        log_metadata = LogMetadata(
            log_id=str(execute_id),
            group_id=str(self.id),
            parent_log_id=str(self.last_execute_id)
            if self.last_execute_id is not None
            else None,
        )
        if isinstance(input, (NomosTask, TaskFunctionResponse)):
            variables = variables if variables is not None else {}
            result = input.execute(
                history=self.history,
                variables=variables,
                log_metadata=log_metadata,
            )
        else:
            result = input.execute(
                client=self.client, history=self.history, log_metadata=log_metadata
            )

        self.history = result.history
        self.last_execute_id = execute_id
        return result.data


class Thread:
    def __init__(self, client: "Nomos"):
        self.client = client

    def create(self) -> NomosThread:
        return NomosThread(
            client=self.client,
            history=[],
        )
