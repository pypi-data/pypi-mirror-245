from pydantic import BaseModel, Field

from typing import List, Optional, Dict, Any


class GenerationParams(BaseModel):
    messages: Optional[List[Dict[str, str]]] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = None
    n: Optional[int] = None
    user: Optional[str] = None
    prompt: Optional[str] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    functions: Optional[List[str]] = []
    function_call: Optional[str] = None


class ModelGenerationRequest(BaseModel):
    model_name: str = Field(alias='modelName')
    provider_name: str = Field(alias='providerName')
    order: int = Field(int)
    prompt_params: Optional[GenerationParams] = Field(default={}, alias="promptParams")

    class Config:
        populate_by_name = True

class Usage(BaseModel):
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

class Choice(BaseModel):
    index: int
    text: str
    finish_reason: str
    role: Optional[str] = None
    function_call: Optional[Any] = None
    

class GenerationResponse(BaseModel):
    id: str
    choices: List[Choice]
    model: str
    provider_id: Optional[str] = Field(None, alias='providerId')
    model_id: Optional[str] = Field(None, alias='modelId')
    meta: Optional[Usage]


class ChunkedGenerationResponse(BaseModel):
    event: str
    data: dict
