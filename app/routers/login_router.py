from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.login_schema import LoginForm, LoginResponse
from app.controllers.auth_controller import authenticate_user
from app.utils.jwt_util import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/", response_model=LoginResponse)
def login_user(
    form: LoginForm,
    response: Response,
    db: Session = Depends(get_db)
) -> LoginResponse:
    user, is_admin = authenticate_user(form, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="아이디 또는 비밀번호가 올바르지 않습니다"
        )
    
    access_token = create_access_token(
        data={"sub": user.name},
        expires_delta=timedelta(hours=24),
        is_admin=is_admin
    )
    
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        max_age=86400  
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
        is_admin=is_admin
    )