from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class ExamSchedule(Base):
    __tablename__ = "exam_schedules"

    exam_schedule_id = Column(Integer, primary_key=True, index=True)
    exam_info_id = Column(String, index=True)
    start_time = Column(Date)
    end_time = Column(Date)
    created_at = Column(Date)