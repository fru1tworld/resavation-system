from sqlalchemy import Column, Integer, DateTime
from app.db.session import Base

class ExamSchedule(Base):
    __tablename__ = "exam_schedule"

    exam_schedule_id = Column(Integer, primary_key=True, index=True)
    exam_info_id = Column(Integer, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime)