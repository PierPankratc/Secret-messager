import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.crypto import fernet
from src.db.create_db import get_db
from src.db.models import Messages, Users
from src.routers.users import get_current_user

router = APIRouter(prefix="/link")


@router.get("/{link_id}", status_code=200)
def read_message_link(link_id: str, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    link_uuid = uuid.UUID(link_id)
    link = db.get(Users, link_uuid)
    if not link or link.user != "link":
        raise HTTPException(status_code=404, detail="link not found")

    try:
        message_uuid = uuid.UUID(link.hached_passwd)
    except ValueError:
        raise HTTPException(status_code=404, detail="message not found")

    message = db.get(Messages, message_uuid)
    if not message:
        raise HTTPException(status_code=404, detail="message not found")

    db.delete(link)
    db.delete(message)
    db.commit()
    return {"id": message.id, "message": fernet.decrypt(message.encrypted_message.encode()).decode()}
