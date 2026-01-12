from pydantic import BaseModel,ConfigDict
from typing import Optional


"""pydanric schemas to validate the input and output"""

# input valiation
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None

# output valiation
class ChatResponse(BaseModel):
    message: str
    session_id: int

    """By default pydantic expects data to be parsed as dict so ConfigDict allows your model to read data from objects, not just dict."""
    model_config = ConfigDict(from_attributes=True)