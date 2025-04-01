from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class ExamCategorie(Base):
    __tablename__ = "exam_categorie"

    exam_categorie_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime)