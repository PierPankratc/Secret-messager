import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.crypto import fernet
from src.db.create_db import get_db
from src.db.models import Messages, Users
from src.routers.users import get_current_user

router = APIRouter(prefix="/message")


@router.post("", status_code=200)
def create_message(payload: dict[str, str], db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    plaintext = payload["message"]
    encrypted = fernet.encrypt(plaintext.encode()).decode()
    message = Messages(encrypted_message=encrypted)
    db.add(message)
    db.commit()
    db.refresh(message)

    link = Users(user="link", hached_passwd=str(message.id))
    db.add(link)
    db.commit()
    db.refresh(link)

    return {
        "id": message.id,
        "message": encrypted,
        "link_id": link.id,
        "link": f"/link/{link.id}",
    }


@router.post("/{message_id}/link", status_code=200)
def create_message_link(message_id: str, db: Session = Depends(get_db)):
    message_uuid = uuid.UUID(message_id)
    message = db.get(Messages, message_uuid)
    if not message:
        raise HTTPException(status_code=404, detail="message not found")

    link = Users(user="link", hached_passwd=str(message_uuid))
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"id": link.id, "message_id": message_id, "link": f"/link/{link.id}"}


@router.get("/{message_id}", status_code=200)
def get_message(message_id: str, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    message = db.get(Messages, uuid.UUID(message_id))
    if not message:
        raise HTTPException(status_code=404, detail="message not found")
    return {"id": message.id, "message": fernet.decrypt(message.encrypted_message.encode()).decode()}
