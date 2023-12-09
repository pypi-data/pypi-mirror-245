from typing import TYPE_CHECKING, List
from nomos.api_resources.models.azure_open_ai_chat_completion_params import (
    AzureOpenAIChatCompletionParams,
)
from nomos.api_resources.models.open_ai_chat_completion_params import (
    OpenAIChatCompletionParams,
)
from nomos.api_resources.models.task import Task
from nomos.resources.logger import NomosLogger
from nomos.resources.prompt_parser import PromptParser
from nomos.resources.tasks.providers.azure_openai import AzureOpenai
from nomos.resources.tasks.providers.openai import Openai
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from nomos.resources.types import (
    FunctionResponse,
    ExecuteResult,
    LogMetadata,
    TaskLogMetadata,
    TaskLogMetadataWithVariables,
)

from nomos.resources.variable_parser import VariablesData

# Avoids circular import issues with typing
if TYPE_CHECKING:
    from ..client import Nomos


class NomosTask:
    def __init__(
        self,
        client: "Nomos",
        project_id: str,
        project_version_id: str,
        task: Task,
    ):
        self.client = client
        self.project_id = project_id
        self.project_version_id = project_version_id
        self.task = task

    def llm(self):
        if isinstance(self.task.parameters.actual_instance, OpenAIChatCompletionParams):
            if self.client.openai_client is None:
                raise ValueError(
                    "OpenAI client is not configured. Please set the OPENAI_API_KEY environment variable"
                )
            return Openai(
                client=self.client.openai_client,
                nomos_logger=NomosLogger(
                    nomos_api=self.client.nomos_api,
                ),
            )
        elif isinstance(
            self.task.parameters.actual_instance, AzureOpenAIChatCompletionParams
        ):
            if self.client.azure_openai_client is None:
                raise ValueError(
                    "Azure OpenAI client is not configured. Please set the AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables"
                )
            return AzureOpenai(
                client=self.client.azure_openai_client,
                nomos_logger=NomosLogger(
                    nomos_api=self.client.nomos_api,
                ),
                endpoint=self.client.azure_endpoint,
            )
        else:
            raise ValueError(f"Parameters {self.task.parameters} is not supported")

    def variables(self) -> List[str]:
        variables = PromptParser.get_variables(
            self.task.prompt_template.actual_instance
        )
        variables.update(
            self.llm().get_parameter_variables(
                parameters=self.task.parameters.actual_instance
            )
        )
        return variables

    def execute(
        self,
        history: List[ChatCompletionMessageParam],  # need to add history
        variables: VariablesData,
        log_metadata: LogMetadata,
    ) -> ExecuteResult:
        llm = self.llm()
        parsed_parameters = llm.parse_parameters(
            parameters=self.task.parameters.actual_instance,
            variables=variables,
        )
        return llm.execute_prompt(
            prompt=self.task.prompt_template.actual_instance,
            parameters=parsed_parameters,
            chat_history=history,
            variables=variables,
            log_metadata=TaskLogMetadata(
                **log_metadata,
                task_id=self.task.id,
                project_id=self.project_id,
                project_version_id=self.project_version_id,
            ),
        )

    def create_function_response(
        self,
        name: str,
        response: str,
    ) -> "TaskFunctionResponse":
        return TaskFunctionResponse(
            client=self.client,
            project_id=self.project_id,
            project_version_id=self.project_version_id,
            task=self.task,
            function_response=FunctionResponse(
                name=name,
                response=response,
            ),
        )


class TaskFunctionResponse(NomosTask):
    def __init__(
        self,
        client: "Nomos",
        project_id: str,
        project_version_id: str,
        task: Task,
        function_response: FunctionResponse,
    ):
        super().__init__(client, project_id, project_version_id, task)
        self.function_response = function_response

    def execute(
        self,
        history: List[ChatCompletionMessageParam],  # need to add history
        variables: VariablesData,
        log_metadata: LogMetadata,
    ) -> ExecuteResult:
        llm = self.llm()
        parsed_parameters = llm.parse_parameters(
            parameters=self.task.parameters.actual_instance,
            variables=variables,
        )
        return llm.send_function_response(
            parameters=parsed_parameters,
            chat_history=history,
            function_response=self.function_response,
            log_metadata=TaskLogMetadataWithVariables(
                **log_metadata,
                variables=variables,
                task_id=self.task.id,
                project_id=self.project_id,
                project_version_id=self.project_version_id,
            ),
        )
