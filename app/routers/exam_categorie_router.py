from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_categorie_schema import ExamCategorieCreateRequest, ExamCategorieResponse
from app.controllers.exam_categorie_controller import create_exam_categorie, read_exam_categorie, delete_exam_categorie

router = APIRouter()

@router.post("/adm")
def create_exam_categorie_router(
    req: ExamCategorieCreateRequest,
    db: Session = Depends(get_db)
) -> ExamCategorieResponse:
    return create_exam_categorie(req, db)

@router.get("/")
def read_exam_categorie_router(
    id: int = Query(..., description="조회할 카테고리의 ID"),
    db: Session = Depends(get_db)
) -> ExamCategorieResponse:
    return read_exam_categorie(id, db)

@router.delete("/adm")
def delete_exam_categorie_router(
    request: Request,
    id: int = Query(..., description="삭제할 카테고리의 ID"),
    db: Session = Depends(get_db)
):
    user_role = request.state.user_role
    return delete_exam_categorie(id, db, user_role)