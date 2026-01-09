from pydantic import BaseModel,ConfigDict

"""pydanric schemas to validate the input and output"""

# input valiation
class ChatRequest(BaseModel):
    user_id: int
    message: str

# output valiation
class ChatResponse(BaseModel):
    message: str

    """By default pydantic expects data to be parsed as dict so ConfigDict allows your model to read data from objects, not just dict."""
    model_config = ConfigDict(from_attributes=True)
