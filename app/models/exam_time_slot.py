from sqlalchemy import Column, Integer, Date, DateTime
from app.db.session import Base

class ExamTimeSlot(Base):
    __tablename__ = "exam_time_slot"

    exam_time_slot_id = Column(Integer, primary_key=True, index=True)
    exam_date = Column(Date)  
    time_slot = Column(Integer)
    examinee_count = Column(Integer, default=0)
    created_at = Column(DateTime)