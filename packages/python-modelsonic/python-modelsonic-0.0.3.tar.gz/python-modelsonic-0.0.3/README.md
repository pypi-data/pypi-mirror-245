# ModelSonic Python Client

This is a Python client for the ModelSonic APIs.

## Installation

Use the package manager [pip](https://pypi.org/en/stable) to install python-modelsonic.

```bash
pip install python-modelsonic
```

## Usage

```python
from modelsonic.client import ModelSonicClient
from modelsonic.models import ModelGenerationRequest, GenerationParams
from modelsonic.enums import ModelsEnum, ProvidersEnum


client = ModelSonicClient(base_url='your_base_url', api_key='your_api_key')

messages = [
    {"role": "user", "content": "Write me a short poem"},
]
prompt_params = GenerationParams(messages=messages)
claude2_request = ModelGenerationRequest(
    model_name=ModelsEnum.CLAUDE_INSTANT_12,
    provider_name=ProvidersEnum.ANTHROPIC.value,
    order=1,
    prompt_params=prompt_params,
)

response = client.generate(ordered_generation_requests=[claude2_request])
print(response.choices[0].text)
```

Remember to replace `'your_base_url'` and `'your_api_key'` with your actual base URL and API key when using the client.