from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class ExamInfo(Base):
    __tablename__ = "exam_info"

    exam_info_id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String, index=True)
    exam_description = Column(String)
    exam_category_id = Column(Integer)
    created_at = Column(DateTime)