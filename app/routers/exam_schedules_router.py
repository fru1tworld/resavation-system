from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_schedule_schema import ExamScheduleCreateRequest, ExamScheduleResponse
from app.controllers.exam_schedule_controller import create_exam_schedule, read_exam_schedule

router = APIRouter()

@router.post("/adm")
def create_exam_schedule_router(
    req: ExamScheduleCreateRequest,
    request: Request,
    db: Session = Depends(get_db)
) -> ExamScheduleResponse:
    return create_exam_schedule(req, db)

@router.get("/")
def read_exam_schedule_router(
    id: int = Query(..., description="조회할 시험 일정의 ID"),  
    db: Session = Depends(get_db)
) -> ExamScheduleResponse:
    return read_exam_schedule(id, db)