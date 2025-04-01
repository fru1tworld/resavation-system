from sqlalchemy import Column, Integer, Date
from app.db.session import Base

class ExamineeCount(Base):
    __tablename__ = "exam_time_slot"

    examinee_count_id = Column(Integer, primary_key=True, index=True)
    exam_schedule_id = Column(Integer)
    examinee_count = Column(Integer)
