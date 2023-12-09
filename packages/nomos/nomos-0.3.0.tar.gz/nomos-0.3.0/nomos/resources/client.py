import os
from typing import Optional
from nomos import NomosApi, ApiClient, Configuration, Project
from openai import (
    OpenAI,
    AzureOpenAI,
)

from nomos.resources.messages.message import Message
from nomos.resources.thread import Thread


class Nomos:
    def __init__(
        self,
        client_id: Optional[str] = os.environ.get("NOMOS_CLIENT_ID"),
        secret: Optional[str] = os.environ.get("NOMOS_SECRET"),
        openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY"),
        openai_organization: Optional[str] = os.environ.get("OPENAI_ORG_ID"),
        azure_openai_api_key: Optional[str] = os.environ.get("AZURE_OPENAI_API_KEY"),
        azure_endpoint: Optional[str] = os.environ.get("AZURE_OPENAI_ENDPOINT"),
    ):
        if client_id is None or secret is None:
            raise ValueError(
                "Missing NOMOS_CLIENT_ID or NOMOS_SECRET. either provide it, or instantiate the Nomos client with options, like Nomos(client_id='my nomos client_id',secret='my nomos secret')."
            )
        self.client_id = client_id
        self.secret = secret
        self.openai_api_key = openai_api_key
        self.openai_organization = openai_organization
        self.azure_openai_api_key = azure_openai_api_key
        self.azure_endpoint = azure_endpoint

        # Initialize Nomos API
        configuration = Configuration(
            api_key={
                "clientId": self.client_id,
                "secret": self.secret,
            }
        )
        api_client = ApiClient(configuration=configuration)
        self.nomos_api = NomosApi(api_client=api_client)

        # Initialize Resources
        self.project = Project(self)
        self.message = Message(self)
        self.thread = Thread(self)

        # Initialize OpenAI client
        self.openai_client = None
        if self.openai_api_key is not None:
            self.openai_client = OpenAI(
                api_key=self.openai_api_key,
                organization=self.openai_organization,
            )

        # Initialize Azure OpenAI client
        self.azure_openai_client = None
        if self.azure_openai_api_key is not None and self.azure_endpoint is not None:
            self.azure_openai_client = AzureOpenAI(
                api_key=self.azure_openai_api_key,
                # Set using the latest version available as of 10/12/2023 and will upgrade this as needed in the future.
                # For available versions, see:
                # https://github.com/Azure/azure-rest-api-specs/tree/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview
                api_version="2023-09-01-preview",
                azure_endpoint=self.azure_endpoint,
                organization=self.openai_organization,
            )
