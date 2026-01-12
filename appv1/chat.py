from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from appv1 import models, schemas
from appv1.mysql_database import get_db
from appv1.prompt import MEDICAL_CODING_PROMPT
from appv1.llm import llm
import traceback

router = APIRouter()

@router.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    try:
        # use existing session or create new
        if request.session_id:
            session_obj = db.get(models.ChatSession, request.session_id)
            if not session_obj:
                raise HTTPException(status_code=404, detail="Session not found")
        else:
            session_obj = models.ChatSession()
            db.add(session_obj)
            db.commit()
            db.refresh(session_obj)

        # store user message
        user_msg = models.Message(
            session_id=session_obj.id,
            sender="user",
            content=request.message
        )
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        # call LLM
        try:
            ai_message = llm.invoke(MEDICAL_CODING_PROMPT.format(user_input=request.message))
            response_text = ai_message.content
        except Exception as e:
            response_text = f"LLM error: {str(e)}"

        # bot message storage
        bot_msg = models.Message(
            session_id=session_obj.id,
            sender="bot",
            content=response_text
        )
        db.add(bot_msg)
        db.commit()
        db.refresh(bot_msg)

        # message + session_id
        return schemas.ChatResponse(
            message=response_text,
            session_id=session_obj.id
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
