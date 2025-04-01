from sqlalchemy.orm import Session
from app.models.exam_schedule import ExamSchedule
from app.models.exam_info import ExamInfo
from datetime import datetime, timezone
from app.schemas.exam_schedule_schema import ExamScheduleCreateRequest, ExamScheduleResponse
from app.utils.snowflake import generate_snowflake_id
from app.controllers.exam_time_slot_controller import create_exam_time_slots
from fastapi import HTTPException, status

def create_exam_schedule(req: ExamScheduleCreateRequest, db: Session) -> ExamScheduleResponse:
    exam_info = db.query(ExamInfo).filter(ExamInfo.exam_info_id == req.exam_info_id).first()
    if not exam_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 정보를 찾을 수 없습니다.")
        
    if req.start_time >= req.end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시작 시간은 종료 시간보다 이전이어야 합니다.")
        
    db_exam_schedule = ExamSchedule(
        exam_schedules_id=generate_snowflake_id(),
        exam_info_id=req.exam_info_id,
        start_time=req.start_time,
        end_time=req.end_time,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_exam_schedule)
    db.commit()
    db.refresh(db_exam_schedule)
    
    create_exam_time_slots(db_exam_schedule.exam_schedules_id, db)
    
    return db_exam_schedule

def read_exam_schedule(id: int, db: Session) -> ExamScheduleResponse:
    db_exam_schedule = db.query(ExamSchedule).filter(ExamSchedule.exam_schedules_id == id).first()
    if not db_exam_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 일정을 찾을 수 없습니다.")
    return db_exam_schedule