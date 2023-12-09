# rebyte-langchain

rebyte-langchain is a Python library to access the ReByte Agent REST API. This library enables you to use rebyte in a langchain-like style.

## Features

1. Generate streaming or non-streaming output.
2. Use async or sync method.
3. Compatiable with langchain callback functions.
4. Support stateful agent memory with session_id.

## Install
```shell
pip install rebyte_langchain
```

## Simple Demo

```python
# import packages
from endpoint.rebyte import RebyteEndpoint
import os
import asyncio
from langchain.schema.messages import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# required keys & config
# You can set REBYTE_API_KEY as an environment variable 
os.environ['REBYTE_API_KEY'] = "<rebyte_api_key>"
# Or pass it as an argument to the RebyteEndpoint constructor
test_rebyte_api_key:str = "<rebyte_api_key>"

# create an agent on rebyte platform and get the project_id and callable_id
# https://rebyte.ai/api/sdk/p/{test_project_id}/a/{test_callable_id}/r
test_project_id:str = "<test_project_id>"
test_callable_id:str = "<test_callable_id>"

# You may use any string as session_id 
# Note that you must set session_id if you use any states ("memory") in your agent, such as KV storage. Otherwise, the agent will raise error
# Or you can leave it as None when the agent has no states. The system will generate a random session_id for you.
test_session_id:str = None

# test input
human_messages = [HumanMessage(content="Who are you")]

def generate(stream = False):
  model = RebyteEndpoint(
    rebyte_api_key=test_rebyte_api_key,
    project_id=test_project_id,
    callable_id=test_callable_id,
    session_id=test_session_id,
    streaming=stream
  )
  response = model.generate([human_messages],
                            callbacks=[StreamingStdOutCallbackHandler()]
                            )
  return response

async def agenerate(stream = False):
  model = RebyteEndpoint(
    rebyte_api_key=test_rebyte_api_key,
    project_id=test_project_id,
    callable_id=test_callable_id,
    session_id=test_session_id,
    streaming=stream
  )
  response = await model.agenerate(messages=
                                   [human_messages],
                                   callbacks=[StreamingStdOutCallbackHandler()]
                                   )
  return response

if __name__ == "__main__":
  print("\n\nTEST GENERATE\n\n")
  response = generate(stream=True)

  print("\n\nTEST AGENERATE\n\n")
  loop = asyncio.get_event_loop()
  loop.run_until_complete(agenerate(stream=True))
```

Please see more examples in main.py and example.ipynb.

## Documentation

More information can be found on the [ReByte Documentation Site](https://rebyte-ai.gitbook.io/rebyte/).
