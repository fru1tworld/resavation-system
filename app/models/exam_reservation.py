from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class ExamReservation(Base):
    __tablename__ = "exam_reservation"

    exam_reservation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    exam_schedule_id = Column(Integer)
    reservation_status = Column(String)
    created_at = Column(DateTime)