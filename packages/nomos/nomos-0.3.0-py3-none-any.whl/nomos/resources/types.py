from typing import List, Optional, NamedTuple
from openai.types.chat.chat_completion import ChatCompletion
from nomos.resources.variable_parser import VariablesData
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class ChatCompletionMessage(TypedDict, total=False):
    role: str
    content: Optional[str]
    function_call: Optional[dict]
    name: Optional[str]


class FunctionResponse(TypedDict):
    name: str
    response: str


class ExecuteResult(NamedTuple):
    history: List[ChatCompletionMessageParam]
    data: ChatCompletion


class LogMetadata(TypedDict):
    log_id: str
    group_id: str
    parent_log_id: Optional[str]


class TaskLogMetadata(LogMetadata):
    task_id: str
    project_id: str
    project_version_id: str


class TaskLogMetadataWithVariables(TaskLogMetadata):
    variables: VariablesData
