"""
Nomos Simple Example

### Introduction ###
This example corresponds to the simple example on the Nomos dashboard. To see
the prompt template being used for this example, please go to:
app.getnomos.com > Examples > 1. Simple (one task) project

### Setting NOMOS_CLIENT_ID, NOMOS_SECRET, and OPENAI_API_KEY ###
There are two ways to set NOMOS_CLIENT_ID, NOMOS_SECRET, and OPENAI_API_KEY. 
You can choose the best option for your application:

1. Set them as environment variables:
    export NOMOS_CLIENT_ID=<YOUR-NOMOS-CLIENT-ID>
    export NOMOS_SECRET=<YOUR-NOMOS-SECRET-KEY>
    export OPENAI_API_KEY=<YOUR-OPENAI-API-KEY>

2. When initializing the Nomos client, pass them as arguments:
    const client = Nomos(
      client_id="<YOUR-NOMOS-CLIENT-ID>",
      secret="<YOUR-NOMOS-SECRET-KEY>",
      openai_api_key="<YOUR-OPENAI-API-KEY>",
    );

### Let's run the example! ###
To run the example, follow the steps below:

1. Replace <YOUR-NOMOS-SIMPLE-EXAMPLE-PROJECT-ID-HERE> below with the actual project_id.
    You can find your project_id by going to 
    app.getnomos.com > Examples > 1. Simple (one task) project
    and copy the project_id at the top of the page.

2. Run with `python3 -m examples.1_simple`

Note try to specify imports to only the classes you need vs running
```
import nomos *
```
"""

from typing import List

from nomos.resources.project import NomosTask
from nomos import Nomos
from pprint import pprint

client = Nomos()

project = client.project.get(
    project_id="<YOUR-NOMOS-SIMPLE-EXAMPLE-PROJECT-ID-HERE>",
)
tasks: List[NomosTask] = project.get_tasks()

if len(tasks) == 0:
    raise Exception("No tasks found")

thread = client.thread.create()
for i, task in enumerate(tasks):
    pprint(f"###################### Start of Task {i+1} ######################")
    data = thread.execute(
        input=task,
        variables={
            "topic": "China",
            "max_words": 5,
            "question": "What is the capital of China?",
            "state": "CA",
        },
    )
    pprint(data)
    pprint(f"###################### End of Task {i+1} ######################")


pprint("###################### Chat History ######################")
pprint(thread.history)
pprint("###################### End of Chat History ######################")

data = thread.execute(
    input=client.message.azure_openai.create(
        {
            "deployment_name": "gpt-35-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": "Is it the largest city in the country?",
                }
            ],
        }
    )
)
pprint(data)
pprint(thread.history)
