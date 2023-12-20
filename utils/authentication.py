import sqlite3
from fastapi import HTTPException,status
from datetime import datetime, timedelta
from jose import jwt
from config import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, USER_DATABASE
from database.userdatastore import UserDataStore
from utils.password_hasher import verify_password



def validate_jwt(token: str) -> str:
    decoded_jwt :dict = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    return decoded_jwt

def create_access_token(username: str,role : str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "role": role,"sub":username}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt


async def authenticate_user(form_data):
    with sqlite3.connect(USER_DATABASE) as conn :
        repo = UserDataStore(conn)
        user = await repo.check_email_id(email_id=form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(form_data.password, user['password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            username= user['email'],role=user["role"], expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}





