from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.login_schema import LoginForm
from app.schemas.login_schema import LoginResponse
from app.utils.bcrypt_util import verify_password

def authenticate_user(db: Session, login: LoginForm) -> LoginResponse:
    db_user = db.query(User).filter(User.name == login.name).first()
    if not db_user:
        return False, None

    if verify_password(login.password, db_user.password):
        return LoginResponse.model_validate(db_user)

    return False, None
