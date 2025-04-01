from sqlalchemy.orm import Session
from app.models.exam_schedule import ExamSchedule
from datetime import datetime, timezone
from app.schemas.exam_schedule_schema import ExamScheduleCreateRequest, ExamScheduleResponse
from app.utils.snowflake import generate_snowflake_id

def create_exam_schedule(exam: ExamScheduleCreateRequest, db: Session) -> ExamScheduleResponse:
    db_exam_schedule = ExamSchedule(exam_schedule_id=generate_snowflake_id(), 
                             exam_name=exam.name,
                             description=exam.description, 
                             category_id=exam.category_id,
                             created_at=datetime.now(timezone.utc)
                             )
    db.add(db_exam_schedule)
    db.commit()
    db.refresh(db_exam_schedule)
    return db_exam_schedule

def read_exam_schedule(id: int, db: Session) -> ExamScheduleResponse:
    db_exam_schedule = db.query(ExamSchedule).where(ExamSchedule.exam_schedule_id == id).first()
    return db_exam_schedule
