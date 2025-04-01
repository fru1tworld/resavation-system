from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_info_schema import ExamInfoCreateRequest, ExamInfoResponse
from app.controllers.exam_info_controller import create_exam_info, read_exam_info, delete_exam_info

router = APIRouter()

@router.post("/adm")
def create_exam_info_router(
    req: ExamInfoCreateRequest, 
    db: Session = Depends(get_db)
) -> ExamInfoResponse:
    return create_exam_info(req, db)

@router.get("/")
def read_exam_info_router(
    id: int = Query(..., description="조회할 시험 정보의 ID"),  
    db: Session = Depends(get_db)
) -> ExamInfoResponse:
    return read_exam_info(id, db)

@router.delete("/adm")
def delete_exam_info_router(
    request: Request,
    id: int = Query(..., description="삭제할 시험 정보의 ID"),
    db: Session = Depends(get_db)
):
    user_role = request.state.user_role
    return delete_exam_info(id, db, user_role)