# Nomos

[![Visit Us](https://img.shields.io/badge/visit_us-nomos-orange)](https://docs.getnomos.com) [![documentation](https://img.shields.io/badge/docs-docs?label=documentation)](https://docs.getnomos.com) [![](https://img.shields.io/badge/Join%20our%20community-Discord-blue)](https://discord.gg/xEPFsvSmkb)

Nomos is a Generative AI development platform that empowers teams to create, monitor, and improve their production LLM applications through rigorous data-driven experimentation.

The Nomos Python library provides convenient access to the Nomos SDK and API for applications written in Python.

## Installation

```bash
pip install nomos
```

## Usage

### 1. Authentication

First, get your Nomos client_id and secret from the Nomos dashboard. Go to **Settings > Manage API Keys** and copy your client_id and secret.

- Define them as environment variables.

```bash
export NOMOS_CLIENT_ID="YOUR-NOMOS-CLIENT-ID"
export NOMOS_SECRET="YOUR-NOMOS-SECRET-KEY"
export OPENAI_API_KEY="YOUR-OPENAI-API-KEY"
```

- Or, initialize the Nomos client with client_id and secrets.

```python
client = Nomos(
    client_id="<YOUR-NOMOS-CLIENT-ID>",
    secret="<YOUR-NOMOS-SECRET-KEY>",
    openai_api_key="<YOUR-OPENAI-API-KEY>"
)
```

### 2. Using Nomos in your application

```python
from nomos import Nomos

client = Nomos()

project = client.project.get(project_id="NOMOS-PROJECT-ID")
task = project.get_first_task()
response = task.execute(variables={})

print(response.data)
```

## Documentation

For more information on how to use Nomos and our SDK, please refer to our [documentation](https://docs.getnomos.com/).

## License

[MIT](https://choosealicense.com/licenses/mit/)
