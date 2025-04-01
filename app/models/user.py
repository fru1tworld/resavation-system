from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    role = Column(String)
    created_at = Column(Date)