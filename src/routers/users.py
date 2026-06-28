import os

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from src.db.create_db import get_db
from src.db.models import Users
from src.routers.schemas import Users as UserSchema

router = APIRouter(prefix='/user')


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


@router.post('/register')
def register_user(payload: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.user == payload.user).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='user already exists')

    hashed_password = bcrypt.hashpw(payload.passwd.encode(), bcrypt.gensalt()).decode()
    user = Users(user=payload.user, hached_passwd=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'id': user.id, 'user': user.user}


@router.post('/login')
def login_user(payload: UserSchema, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user == payload.user).first()
    if not user or not _verify_password(payload.passwd, user.hached_passwd or ''):
        raise HTTPException(status_code=401, detail='invalid credentials')

    token = os.urandom(16).hex()
    user.hached_passwd = token
    db.commit()
    return {'access_token': token, 'user': user.user}


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='missing or invalid token')

    token = authorization.split(' ', 1)[1]
    user = db.query(Users).filter(Users.hached_passwd == token).first()
    if not user:
        raise HTTPException(status_code=401, detail='invalid token')
    return user

