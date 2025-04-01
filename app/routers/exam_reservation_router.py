from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_reservation_schema import ExamReservationCreateRequest, ExamReservationResponse
from app.controllers.exam_reservation_controller import create_exam_reservation, read_exam_reservation_detale
router = APIRouter()

@router.post("/adm")
def create_exam_reservation(req: ExamReservationCreateRequest,
                      db: Session = Depends(get_db)) -> ExamReservationResponse:
    return create_exam_reservation(req, db)

@router.get("/")
def read_exam_reservation(id: int = Query(..., description="조회할 테스트 정보의 ID"),  
                   db: Session = Depends(get_db)) -> ExamReservationResponse:
    return read_exam_reservation_detale(id, db)
