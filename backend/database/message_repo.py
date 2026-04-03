from sqlalchemy.orm import Session
from backend.database.message_model import Message


def save_message(db: Session, conversation_id: int, role: str, content: str):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages(db: Session, conversation_id: int):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
        .all()
    )