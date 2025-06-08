from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.sql import func
from source.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID


class Chat(Base):
    """таблица для хранения диалогов с llm агентом"""
    
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id_uuid = Column(UUID, comment="uuid чата")
    message_from_human = Column(Text, comment="сообщение от пользователя")
    message_from_ai_agent = Column(Text, comment="ответ от llm agent")    
    created_at = Column(DateTime, default=func.now(), comment="время создания записи")
