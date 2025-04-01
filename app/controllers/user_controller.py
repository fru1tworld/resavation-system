from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreateRequest, UserResponse
from app.utils.bcrypt_util import hash_password
from app.utils.snowflake import generate_snowflake_id
from datetime import datetime, timezone
from fastapi import HTTPException, status

def create_user(user: UserCreateRequest, db: Session) -> UserResponse:
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 사용자명입니다.")
        
    db_user = User(
        user_id=generate_snowflake_id(),
        name=user.name,
        password=hash_password(user.password),
        role="USER",
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_user(id: int, db: Session) -> UserResponse:
    db_user = db.query(User).filter(User.user_id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    return db_user

def create_adm(user: UserCreateRequest, db: Session) -> UserResponse:
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 사용자명입니다.")
        
    db_user = User(
        user_id=generate_snowflake_id(),
        name=user.name,
        password=hash_password(user.password),
        role="ADMIN",
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user