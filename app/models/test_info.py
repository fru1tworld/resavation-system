from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Test_Info(Base):
    __tablename__ = "test_info"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    role = Column(String)
