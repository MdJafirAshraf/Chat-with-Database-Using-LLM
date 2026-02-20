from pydantic import BaseModel
from typing import Literal


class ChatRequest(BaseModel):
    question: str
    provider: Literal["groq", "gemini"]


class ChatResponse(BaseModel):
    question: str
    sql: str
    answer: str