from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.login_schema import LoginForm
from app.schemas.user_schema import UserResponse
from app.utils.bcrypt_util import verify_password
from fastapi import HTTPException, status

def authenticate_user(form: LoginForm, db: Session) -> Tuple[Optional[UserResponse], bool]:
    db_user = db.query(User).filter(User.name == form.name).first()
    
    if not db_user:
        return None, False
    
    if verify_password(form.password, db_user.password):
        is_admin = db_user.role == "ADMIN"
        return UserResponse.model_validate(db_user), is_admin
    
    return None, False