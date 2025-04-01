from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class ExamReservation(Base):
    __tablename__ = "exam_reservation"

    exam_reservation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    schedule_id = Column(String)
    created_at = Column(Date)
