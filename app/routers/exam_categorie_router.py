from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_categorie_schema import ExamCategorieCreateRequest, ExamCategorieResponse
from app.controllers.exam_categorie_controller import create_exam_categorie, read_exam_categorie
router = APIRouter()

@router.post("/adm")
def create_exam_info(req: ExamCategorieCreateRequest,
                     db: Session = Depends(get_db)) -> ExamCategorieResponse:
    return create_exam_categorie(req, db)


@router.get("/")
def read_exam_info(id: int = Query(...),
                   db: Session = Depends(get_db)) -> ExamCategorieResponse:
    return read_exam_categorie(id, db)
