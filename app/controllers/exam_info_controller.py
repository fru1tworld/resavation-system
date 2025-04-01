from sqlalchemy.orm import Session
from app.models.exam_info import ExamInfo
from app.schemas.exam_info_schema import ExamInfoCreateRequest, ExamInfoResponse
from app.utils.snowflake import generate_snowflake_id
from datetime import datetime, timezone
from fastapi import HTTPException, status

def create_exam_info(exam: ExamInfoCreateRequest, db: Session) -> ExamInfoResponse:
    db_exam_info = ExamInfo(
        exam_info_id=generate_snowflake_id(), 
        exam_name=exam.name,
        description=exam.description, 
        category_id=exam.category_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_exam_info)
    db.commit()
    db.refresh(db_exam_info)
    return db_exam_info

def read_exam_info(id: int, db: Session) -> ExamInfoResponse:
    db_exam_info = db.query(ExamInfo).where(ExamInfo.exam_info_id == id).first()
    if not db_exam_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 정보를 찾을 수 없습니다")
    return db_exam_info

def delete_exam_info(id: int, db: Session, user_role: str):
    if user_role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 시험 정보를 삭제할 수 있습니다")
    
    db_exam_info = db.query(ExamInfo).where(ExamInfo.exam_info_id == id).first()
    if not db_exam_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 정보를 찾을 수 없습니다")
    
    db.delete(db_exam_info)
    db.commit()
    return {"message": "시험 정보가 삭제되었습니다"}