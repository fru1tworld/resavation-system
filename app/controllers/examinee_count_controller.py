from sqlalchemy.orm import Session
from app.models.examinee_count import ExamineeCount

from datetime import datetime
def create_exam_time_slots(start_time: datetime, end_time: datetime, db: Session):
    current_time = start_time

    db.commit()