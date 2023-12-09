from typing import (
    List,
    Optional,
    TYPE_CHECKING,
)

from nomos import (
    ProjectVersionGetActiveRequest,
    ProjectVersion,
    ProjectVersionGetRequest,
)
from nomos.resources.tasks.task import NomosTask

# Avoids circular import issues with typing
if TYPE_CHECKING:
    from .client import Nomos


class NomosProject:
    def __init__(self, client: "Nomos", project_version: ProjectVersion):
        self.client = client
        self.project_version = project_version

    """Gets the list of tasks in the project. """

    def get_tasks(self) -> List[NomosTask]:
        tasks = []
        for task in self.project_version.tasks:
            tasks.append(
                NomosTask(
                    client=self.client,
                    project_id=self.project_version.project_id,
                    project_version_id=self.project_version.id,
                    task=task,
                )
            )

        return tasks


class Project:
    def __init__(self, client: "Nomos"):
        self.client = client

    def get(self, project_id: str, branch: Optional[str] = None) -> NomosProject:
        body = (
            ProjectVersionGetActiveRequest(
                project_id=project_id,
                branch_name=branch,
            )
            if branch is not None
            else ProjectVersionGetActiveRequest(project_id=project_id)
        )
        response = self.client.nomos_api.project_version_get_active(body)
        return NomosProject(
            client=self.client, project_version=response.project_version
        )

    def get_version(self, project_version_id: str) -> NomosProject:
        body = ProjectVersionGetRequest(
            project_version_id=project_version_id,
        )
        response = self.client.nomos_api.project_version_get(body)
        return NomosProject(
            client=self.client, project_version=response.project_version
        )
