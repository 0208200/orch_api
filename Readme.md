# Orchestrator API Python Client

This Python module provides a client for interacting with the UiPath Orchestrator API.

## Features

- Initialize the API client with your client ID, refresh token, and base URL.
- Send requests to the API with any HTTP method and endpoint.
- Retrieve all assets or assets by key.
- Delete assets by key.
- Create assets with various parameters.
- Add items to a queue with various parameters.

## Usage

First, import the module and create an instance of the `OrchApi` class:

```python
from orch_api import OrchApi

api = OrchApi(client_id, refresh_token, base_url)

response,_ = api.get_all_assets()
