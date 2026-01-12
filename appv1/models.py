from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from appv1.mysql_database import Base


class ChatSession(Base):
    __tablename__ = "chat_session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_name = Column(String(255), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("chat_session.id", ondelete="CASCADE"), nullable=False)
    sender = Column(Enum("user", "bot"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    extra_metadata = Column(JSON, nullable=True)

    session = relationship("ChatSession", back_populates="messages")
