from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserCreateRequest, UserResponse
from app.controllers.user_controller import create_user, read_user, create_adm

router = APIRouter()

@router.post("/")
def create_user_router(req: UserCreateRequest,
                       db: Session = Depends(get_db)) -> UserResponse :
    return create_user(req, db)

@router.get("/")
def read_user_router(id: int = Query(...),
                     db: Session = Depends(get_db)) -> UserResponse:
    return read_user(id, db)

@router.post("/adm")
def create_adm_router(req: UserCreateRequest,
                       db: Session = Depends(get_db)) -> UserResponse :
    return create_adm(req, db)