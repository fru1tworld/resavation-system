from sqlalchemy.orm import Session
from app.models.exam_categorie import ExamCategorie
from app.utils.snowflake import generate_snowflake_id
from app.schemas.exam_categorie_schema import ExamCategorieCreateRequest, ExamCategorieResponse
from datetime import datetime, timezone

def create_exam_categorie(req: ExamCategorieCreateRequest, db: Session) -> ExamCategorieResponse:
    db_exam_categorie = ExamCategorie(test_categorie_id=generate_snowflake_id,
                                       name=req.name,
                                       created_at=datetime.now(timezone.utc)
                                       )
    db.add(db_exam_categorie)
    db.commit()
    db.refresh(db_exam_categorie)
    return db_exam_categorie

def read_exam_categorie(id: int, db: Session) ->ExamCategorieResponse:
    db_exam_categorie = db.query(ExamCategorie).where(ExamCategorie.exam_categorie_id == id).first()

    if not db_exam_categorie:
        return 

    return db_exam_categorie
