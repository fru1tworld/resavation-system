from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserRead
from app.controllers.user_controller import create_user

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user_view(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)