from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_info_schema import ExamInfoCreateRequest, ExamInfoResponse
from app.controllers.exam_info_controller import create_exam_info, read_exam_info 
router = APIRouter()

@router.post("/adm")
def create_exam_info(req: ExamInfoCreateRequest, db: Session = Depends(get_db)) -> ExamInfoResponse:
    return create_exam_info(req, db);

@router.get("/")
def read_exam_info(id: int = Query(...),  
                   db: Session = Depends(get_db)) -> ExamInfoResponse:
    return read_exam_info(id, db)

@router.delete("/adm")
def delete_exam_info(id: int = Query(...),
                    db: Session = Depends(get_db)):
    return delete_exam_info(id, db)