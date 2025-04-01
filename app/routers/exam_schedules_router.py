from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_schedule_schema import ExamScheduleCreateRequest, ExamScheduleResponse
from app.controllers.exam_schedule_controller import create_exam_schedule, read_exam_schedule
router = APIRouter()

@router.post("/")
def create_exam_schedule(req: ExamScheduleCreateRequest,
                     db: Session = Depends(get_db)) -> ExamScheduleResponse:
    
    return create_exam_schedule(req, db)

@router.get("/")
def read_exam_schedule(id: int = Query(..., description="조회할 테스트 정보의 ID"),  
                   db: Session = Depends(get_db)) -> ExamScheduleResponse:
    return read_exam_schedule(id, db)
