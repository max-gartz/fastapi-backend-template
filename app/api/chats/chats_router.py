import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, col

from app.api.chats.chats_schema import (
    Chat, ChatCreate, ChatRead, ChatMessage, ChatMessageCreate, ChatMessageRead
)
from app.api.dependencies import get_db_session, get_current_user
from app.api.users.users_schema import User

router = APIRouter(prefix="/users/{user_id}/chats", tags=["chats"])

logger = logging.getLogger(__name__)


@router.post("", response_model=ChatRead)
def create_chat(
        user_id: int,
        chat_data: ChatCreate,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> ChatRead:
    if user_id != current_user.id:
        logger.error("User not authorized to create chat for another user")
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create chat for another user"
        )
    chat = Chat(**chat_data.model_dump(), user_id=user_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return ChatRead(**chat.model_dump())


@router.get("", response_model=List[ChatRead])
def get_chats(
        user_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> List[ChatRead]:
    if user_id != current_user.id:
        logger.error("User not authorized to list chats for another user")
        raise HTTPException(status_code=403, detail="Not authorized to list chats for another user")
    chats = db.exec(select(Chat).where(Chat.user_id == user_id)).all()
    return [ChatRead(**chat.model_dump()) for chat in chats]


@router.delete("/{chat_id}", response_model=ChatRead)
def delete_chat(
        user_id: int,
        chat_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> ChatRead:
    if user_id != current_user.id:
        logger.error("User not authorized to delete chat for another user")
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete chat for another user"
        )
    chat = db.exec(select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)).first()
    if not chat:
        logger.error("Chat not found")
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return ChatRead(**chat.model_dump())


@router.post("/{chat_id}/messages", response_model=ChatMessageRead)
def create_chat_message(
        user_id: int,
        chat_id: int,
        message_data: ChatMessageCreate,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> ChatMessageRead:
    if user_id != current_user.id:
        logger.error("User not authorized to create chat message for another user")
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create chat message for another user"
        )
    chat = db.exec(select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)).first()
    if not chat:
        logger.error("Chat not found")
        raise HTTPException(status_code=404, detail="Chat not found")
    last_message = db.exec(
        (
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(col(ChatMessage.created_at).desc())
        )
    ).first()
    if last_message.role == message_data.role:
        logger.error("Message roles need to alternate between user and assistant")
        raise HTTPException(
            status_code=400,
            detail="Message roles need to alternate between user and assistant"
        )
    chat_message = ChatMessage(**message_data.model_dump(), chat_id=chat.id)
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return ChatMessageRead(**chat_message.model_dump())


@router.get("/{chat_id}/messages", response_model=List[ChatMessageRead])
def get_chat_messages(
        user_id: int,
        chat_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> List[ChatMessageRead]:
    if user_id != current_user.id:
        logger.error("User not authorized to list chat messages for another user")
        raise HTTPException(
            status_code=403,
            detail="Not authorized to list chat messages for another user"
        )
    chat = db.exec(select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)).first()
    if not chat:
        logger.error("Chat not found")
        raise HTTPException(status_code=404, detail="Chat not found")
    chat_messages = db.exec(
        select(ChatMessage).where(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at)
    ).all()
    return [ChatMessageRead(**chat_message.model_dump()) for chat_message in chat_messages]
