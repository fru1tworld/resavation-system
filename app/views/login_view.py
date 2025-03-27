from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.login_schema import LoginForm, LoginResponse
from app.controllers.login_controller import authenticate_user
from app.utils.jwt_util import create_access_token  

router = APIRouter()

@router.post("/", response_model=LoginResponse)
def create_user_view(form: LoginForm, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, form)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.name})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return LoginResponse.model_validate(user)
