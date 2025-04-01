from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class ExamInfo(Base):
    __tablename__ = "exam_info"

    exam_info_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    exam_name = Column(String, index=True)
    description = Column(String)
    category_id = Column(Integer)
    created_at = Column(Date)
