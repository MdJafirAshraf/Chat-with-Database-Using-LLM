from fastapi import APIRouter, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import handle_question

router = APIRouter(prefix="/api")


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = handle_question(
        provider=request.provider,
        question=request.question
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result