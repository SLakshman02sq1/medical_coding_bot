from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import schemas, models
from .prompt import MEDICAL_CODING_PROMPT
from .llm import llm

router = APIRouter()

@router.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    # Create chat session
    session = models.ChatSession(user_id=request.user_id)
    db.add(session)
    db.commit()
    db.refresh(session)

    # Store user message
    user_message = models.Message(
        session_id=session.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # Prepare prompt
    prompt = MEDICAL_CODING_PROMPT.format(user_input=request.message)

    try:
        # ✅ CORRECT ChatGroq usage
        ai_message = llm.invoke(prompt)   # returns AIMessage
        response_text = ai_message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Store assistant message
    assistant_message = models.Message(
        session_id=session.id,
        role="assistant",
        content=response_text
    )
    db.add(assistant_message)
    db.commit()

    return schemas.ChatResponse(message=response_text)
