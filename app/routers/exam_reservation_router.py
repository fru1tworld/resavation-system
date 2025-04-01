from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.exam_reservation_schema import ExamReservationCreateRequest, ExamReservationResponse
from app.controllers.exam_reservation_controller import (
    create_exam_reservation, read_exam_reservation_detale, 
    cancel_reservation, confirm_reservations_batch, 
    update_reservation_status
)

router = APIRouter()

@router.post("/")
def create_exam_reservation_router(
    req: ExamReservationCreateRequest,
    db: Session = Depends(get_db)
) -> ExamReservationResponse:
    return create_exam_reservation(req, db)

@router.get("/")
def read_exam_reservation_router(
    id: int = Query(..., description="조회할 예약 정보의 ID"),  
    db: Session = Depends(get_db)
) -> ExamReservationResponse:
    return read_exam_reservation_detale(id, db)

@router.delete("/cancel")
def cancel_reservation_router(
    id: int = Query(..., description="취소할 예약 ID"),
    user_id: int = Query(..., description="예약자 ID"),
    db: Session = Depends(get_db)
):
    return cancel_reservation(id, user_id, db)

@router.post("/adm/batch-confirm")
def confirm_reservations_batch_router(
    request: Request,
    db: Session = Depends(get_db)
):
    return confirm_reservations_batch(db)

@router.put("/adm/status")
def update_reservation_status_router(
    id: int = Query(..., description="업데이트할 예약 ID"),
    status: str = Query(..., description="변경할 상태 (PENDING, CONFIRM, CANCEL)"),
    request: Request,
    db: Session = Depends(get_db)
):
    user_role = request.state.user_role
    return update_reservation_status(id, status, user_role, db)