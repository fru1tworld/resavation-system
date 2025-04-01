from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.exam_reservation import ExamReservation
from app.models.exam_time_slot import ExamTimeSlot  
from app.models.exam_schedule import ExamSchedule
from app.utils.snowflake import generate_snowflake_id
from app.schemas.exam_reservation_schema import ExamReservationCreateRequest, ExamReservationResponse
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

MAX_CAPACITY = 50000

def create_exam_reservation(req: ExamReservationCreateRequest, db: Session) -> ExamReservationResponse:
    exam_schedule = db.query(ExamSchedule).where(ExamSchedule.exam_schedule_id == req.schedules_id).first()
    if not exam_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 스케줄을 찾을 수 없습니다")
    
    db_exam_reservation = ExamReservation(
        test_reservation_id=generate_snowflake_id(), 
        user_id=req.user_id, 
        exam_schedule_id=req.schedules_id, 
        status="PENDING", 
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(db_exam_reservation)
    db.commit()
    db.refresh(db_exam_reservation)
    return db_exam_reservation

def read_exam_reservation_detale(id: int, db: Session):
    db_test_reservation = db.query(ExamReservation).where(ExamReservation.exam_reservation_id == id).first()
    if not db_test_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약을 찾을 수 없습니다")
    return db_test_reservation


def cancel_reservation(id: int, user_id: int, db: Session):
    reservation = db.query(ExamReservation).where(
        and_(
            ExamReservation.exam_reservation_id == id,
            ExamReservation.user_id == user_id
        )
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약을 찾을 수 없습니다")
    
    exam_schedule = db.query(ExamSchedule).where(ExamSchedule.exam_schedule_id == reservation.exam_schedule_id).first()
    if not exam_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 스케줄을 찾을 수 없습니다")
    
    current_time = datetime.now(timezone.utc)
    if exam_schedule.start_time - current_time < timedelta(days=3):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시험 시작 3일 전에는 취소할 수 없습니다")
    
    if reservation.status == "CONFIRM":
        update_time_slot_counts(reservation.exam_schedule_id, -1, db)
    
    reservation.status = "CANCEL"
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def update_time_slot_counts(schedule_id: int, change: int, db: Session):
    exam_schedule = db.query(ExamSchedule).where(ExamSchedule.exam_schedule_id == schedule_id).first()
    if not exam_schedule:
        return
    
    exam_date = exam_schedule.start_time.date()
    start_slot = (exam_schedule.start_time.hour * 60 + exam_schedule.start_time.minute) 
    end_slot = (exam_schedule.end_time.hour * 60 + exam_schedule.end_time.minute) 
    
    time_slots = (
        db.query(ExamTimeSlot)
        .where(
            and_(
                ExamTimeSlot.exam_date == exam_date,
                ExamTimeSlot.time_slot >= start_slot,
                ExamTimeSlot.time_slot <= end_slot
            )
        )
        .with_for_update()
        .all()
    )
    
    if change > 0:  
        for slot in time_slots:
            if slot.confirm_count + change > MAX_CAPACITY:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"해당 시간대({slot.time_slot // 60}:{slot.time_slot % 60:02d})는 이미 최대 수용 인원에 도달했습니다"
                )
    
    for slot in time_slots:
        slot.confirm_count += change
        db.add(slot)
    
    db.commit()