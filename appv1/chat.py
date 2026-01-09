from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from appv1.mysql_database import get_db
from appv1 import models, schemas
from appv1.prompt import MEDICAL_CODING_PROMPT
from appv1.llm import llm

router = APIRouter()

# ----------------------
# Chat endpoint
# ----------------------
@router.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):

    # 1️⃣ Create a new chat session for this user/message
    session = models.ChatSession(user_id=request.user_id)
    db.add(session)
    db.commit()
    db.refresh(session)

    # 2️⃣ Store user message
    user_message = models.Message(
        session_id=session.id,
        sender="user",  # <-- corrected from role="user"
        content=request.message
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # 3️⃣ Prepare prompt for LLM
    prompt = MEDICAL_CODING_PROMPT.format(user_input=request.message)

    try:
        # 4️⃣ Call the LLM
        ai_message = llm.invoke(prompt)  # returns AIMessage
        response_text = ai_message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 5️⃣ Store assistant message
    assistant_message = models.Message(
        session_id=session.id,
        sender="bot",  # <-- corrected from role="assistant"
        content=response_text
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    # 6️⃣ Return AI response
    return schemas.ChatResponse(message=response_text)
