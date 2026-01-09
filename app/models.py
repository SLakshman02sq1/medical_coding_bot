from sqlalchemy import Column,Integer,String,DateTime,Text,func
from .sqlite_database import Base
from datetime import timezone
from sqlalchemy import ForeignKey


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer,index=True)
    created_at =  Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True,index=True)
    session_id = Column(Integer,ForeignKey("chat_sessions.id"),index=True)
    role = Column(String,index=True)
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())