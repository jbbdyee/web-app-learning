from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1)
    prompt: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str


class ChatLogCreate(BaseModel):
    user_id: str
    prompt: str
    reply: str