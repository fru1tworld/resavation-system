from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreateRequest, UserResponse
from app.utils.bcrypt_util import hash_password
from app.utils.snowflake import generate_snowflake_id
from datetime import datetime, timezone

def create_user(user: UserCreateRequest, db: Session) -> UserResponse:
    db_user = User(user_id=generate_snowflake_id(),
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
    db_user = db.query(User).where(User.user_id == id).first()
    return db_user


def create_adm(user: UserCreateRequest, db: Session) -> UserResponse:
    db_user = User(user_id=generate_snowflake_id(),
                   name=user.name,
                   password=hash_password(user.password),
                   role="ADMIN",
                   created_at=datetime.now(timezone.utc)
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user