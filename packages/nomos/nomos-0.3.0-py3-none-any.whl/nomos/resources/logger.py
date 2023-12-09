from typing import NamedTuple, Optional
from nomos.resources.variable_parser import VariablesData
from nomos.api_resources.api.nomos_api import NomosApi
from nomos import LogCreateRequest, LogCreateResponse
from datetime import datetime, timezone
import json


class Log(NamedTuple):
    log_id: str
    group_id: str
    provider: str
    model: str
    request_path: str
    request_body: str  # should be any json
    response_status: int
    response: str  # should be any json
    request_start_time: datetime
    request_end_time: datetime
    parent_log_id: Optional[str] = None
    project_id: Optional[str] = None
    variables: Optional[VariablesData] = None
    project_version_id: Optional[str] = None
    task_id: Optional[str] = None


class NomosLogger:
    def __init__(self, nomos_api: NomosApi):
        self.nomos_api = nomos_api

    def log(self, data: Log) -> LogCreateResponse:
        # TODO: Add support for project_version_id and task_id
        # after api is updated
        body = LogCreateRequest(
            log_id=data.log_id,
            parent_log_id=data.parent_log_id,
            group_id=data.group_id,
            provider=data.provider,
            model=data.model,
            request_path=data.request_path,
            request_body=data.request_body,
            response_status=data.response_status,
            response=data.response,
            request_start_time=data.request_start_time.replace(
                tzinfo=timezone.utc
            ).isoformat(),
            request_end_time=data.request_end_time.replace(
                tzinfo=timezone.utc
            ).isoformat(),
            variables={
                key: value if isinstance(value, str) else json.dumps(value)
                for key, value in data.variables.items()
            }
            if data.variables is not None
            else None,
            project_id=data.project_id,
        )
        return self.nomos_api.log_create(log_create_request=body)

    def safe_log(self, log: Log) -> Optional[LogCreateResponse]:
        try:
            return self.log(log)
        except Exception:
            return None
