from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import uuid

from source.db.session import get_db
from source.models.chats import Chat

router = APIRouter(tags=["Chats"], prefix="/chats")

class ChatCreateRequest(BaseModel):
    message_from_human: str
    message_from_ai_agent: str
    message_intent: str
    chat_id_uuid: Optional[str] = None

class ChatResponse(BaseModel):
    id: int
    chat_id_uuid: Optional[uuid.UUID]
    message_from_human: str
    message_from_ai_agent: str
    message_intent: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ChatResponse)
async def create_chat(
    chat_request: ChatCreateRequest,
    db_session: Session = Depends(get_db)
):
    if not chat_request.chat_id_uuid:
        chat_request.chat_id_uuid = str(uuid.uuid4())
    
    new_chat_instance = Chat(
        chat_id_uuid=chat_request.chat_id_uuid,
        message_from_human=chat_request.message_from_human,
        message_from_ai_agent=chat_request.message_from_ai_agent,
        message_intent=chat_request.message_intent
    )
    db_session.add(new_chat_instance)
    db_session.commit()
    db_session.refresh(new_chat_instance)
    return new_chat_instance


class ChatResponseList(BaseModel):
    chat_id_uuid: uuid.UUID
    
@router.get("/list", response_model=List[ChatResponseList])
async def get_chats_list(
    db_session: Session = Depends(get_db)
):
    unique_chat_uuids = db_session.query(Chat.chat_id_uuid).distinct().all()
    chat_list = [ChatResponseList(chat_id_uuid=uuid_row[0]) for uuid_row in unique_chat_uuids if uuid_row[0] is not None]
    
    return chat_list


@router.get("/{chat_uuid}", response_model=List[ChatResponse])
async def get_chat_by_uuid(
    chat_uuid: str,
    db_session: Session = Depends(get_db)
):
    chat_history = db_session.query(Chat).filter(Chat.chat_id_uuid == chat_uuid).all()
    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_history

@router.delete("/{chat_uuid}")
async def delete_chat_by_uuid(
    chat_uuid: str,
    db_session: Session = Depends(get_db)
):
    chat_messages = db_session.query(Chat).filter(Chat.chat_id_uuid == chat_uuid).all()
    if not chat_messages:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    for message in chat_messages:
        db_session.delete(message)
    
    db_session.commit()
    return {"message": f"Chat {chat_uuid} deleted successfully"}