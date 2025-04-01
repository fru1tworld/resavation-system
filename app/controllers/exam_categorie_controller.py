from sqlalchemy.orm import Session
from app.models.exam_categorie import ExamCategorie
from app.utils.snowflake import generate_snowflake_id
from app.schemas.exam_categorie_schema import ExamCategorieCreateRequest, ExamCategorieResponse
from datetime import datetime, timezone
from fastapi import HTTPException, status

def create_exam_categorie(req: ExamCategorieCreateRequest, db: Session) -> ExamCategorieResponse:
    existing = db.query(ExamCategorie).filter(ExamCategorie.name == req.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 카테고리 이름입니다")
    
    db_exam_categorie = ExamCategorie(
        exam_categorie_id=generate_snowflake_id(),
        name=req.name,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_exam_categorie)
    db.commit()
    db.refresh(db_exam_categorie)
    return db_exam_categorie

def read_exam_categorie(id: int, db: Session) -> ExamCategorieResponse:
    db_exam_categorie = db.query(ExamCategorie).filter(ExamCategorie.exam_categorie_id == id).first()
    if not db_exam_categorie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 카테고리를 찾을 수 없습니다")
    return db_exam_categorie

def delete_exam_categorie(id: int, db: Session, user_role: str):
    if user_role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 카테고리를 삭제할 수 있습니다")
    
    db_exam_categorie = db.query(ExamCategorie).filter(ExamCategorie.exam_categorie_id == id).first()
    if not db_exam_categorie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 카테고리를 찾을 수 없습니다")
    
    exam_info = db.query(ExamInfo).filter(ExamInfo.exam_category_id == id).first()
    if exam_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                           detail="이 카테고리를 사용하는 시험 정보가 있어 삭제할 수 없습니다")
    
    db.delete(db_exam_categorie)
    db.commit()
    return {"message": "시험 카테고리가 삭제되었습니다"}