from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.bcrypt_util import hash_password
from app.utils.snowflake import generate_snowflake_id

def create_user(db: Session, user: UserCreate):
    db_user = User(user_id=generate_snowflake_id(), name=user.name, password=hash_password(user.password), role="USER")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user