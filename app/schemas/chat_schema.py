from pydantic import BaseModel
from typing import Literal


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    sql: str
    answer: str