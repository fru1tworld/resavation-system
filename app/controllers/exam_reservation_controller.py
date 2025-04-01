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
    exam_schedule = db.query(ExamSchedule).filter(ExamSchedule.exam_schedules_id == req.exam_schedule_id).first()
    if not exam_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 스케줄을 찾을 수 없습니다")
    
    existing_reservation = db.query(ExamReservation).filter(
        and_(
            ExamReservation.user_id == req.user_id,
            ExamReservation.exam_schedule_id == req.exam_schedule_id,
            ExamReservation.reservation_status != "CANCEL"
        )
    ).first()
    
    if existing_reservation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 동일한 시험 스케줄에 예약이 있습니다")
    
    db_exam_reservation = ExamReservation(
        exam_reservations_id=generate_snowflake_id(), 
        user_id=req.user_id, 
        exam_schedule_id=req.exam_schedule_id, 
        reservation_status="PENDING", 
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(db_exam_reservation)
    db.commit()
    db.refresh(db_exam_reservation)
    return db_exam_reservation

def read_exam_reservation_detale(id: int, db: Session):
    db_exam_reservation = db.query(ExamReservation).filter(ExamReservation.exam_reservations_id == id).first()
    if not db_exam_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약을 찾을 수 없습니다")
    return db_exam_reservation

def cancel_reservation(id: int, user_id: int, db: Session):
    reservation = db.query(ExamReservation).filter(
        and_(
            ExamReservation.exam_reservations_id == id,
            ExamReservation.user_id == user_id
        )
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약을 찾을 수 없습니다")
    
    if reservation.status == "CANCEL":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 취소된 예약입니다")
    
    exam_schedule = db.query(ExamSchedule).filter(ExamSchedule.exam_schedules_id == reservation.exam_schedule_id).first()
    if not exam_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 스케줄을 찾을 수 없습니다")
    
    current_time = datetime.now(timezone.utc)
    if exam_schedule.start_time - current_time < timedelta(days=3):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시험 시작 3일 전에는 취소할 수 없습니다")
    
    if reservation.reservation_status == "CONFIRM":
        update_time_slot_counts(reservation.exam_schedule_id, -1, db)
    
    reservation.reservation_status = "CANCEL"
    db.commit()
    db.refresh(reservation)
    return reservation

def update_time_slot_counts(schedule_id: int, change: int, db: Session):
    exam_schedule = db.query(ExamSchedule).filter(ExamSchedule.exam_schedules_id == schedule_id).first()
    if not exam_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 스케줄을 찾을 수 없습니다")
    
    exam_date = exam_schedule.start_time.date()
    start_slot = (exam_schedule.start_time.hour * 60 + exam_schedule.start_time.minute) 
    end_slot = (exam_schedule.end_time.hour * 60 + exam_schedule.end_time.minute) 
    
    time_slots = (
        db.query(ExamTimeSlot)
        .filter(
            and_(
                ExamTimeSlot.exam_date == exam_date,
                ExamTimeSlot.time_slot >= start_slot,
                ExamTimeSlot.time_slot <= end_slot
            )
        )
        .with_for_update()
        .all()
    )
    
    if not time_slots:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시간 슬롯을 찾을 수 없습니다")
    
    if change > 0:  
        for slot in time_slots:
            if slot.examinee_count + change > MAX_CAPACITY:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"해당 시간대({slot.time_slot // 60}:{slot.time_slot % 60:02d})는 이미 최대 수용 인원에 도달했습니다"
                )
    
    for slot in time_slots:
        slot.examinee_count += change
        if slot.examinee_count < 0:
            slot.examinee_count = 0
    
    db.commit()

def confirm_reservations_batch(db: Session):
    pending_reservations = (
        db.query(ExamReservation)
        .filter(ExamReservation.reservation_status == "PENDING")
        .order_by(ExamReservation.created_at)
        .all()
    )
    
    results = {
        "confirmed": 0,
        "cancelled": 0,
        "total": len(pending_reservations)
    }
    
    for reservation in pending_reservations:
        try:
            exam_schedule = (
                db.query(ExamSchedule)
                .filter(ExamSchedule.exam_schedules_id == reservation.exam_schedule_id)
                .first()
            )
            if not exam_schedule:
                continue
            
            exam_date = exam_schedule.start_time.date()
            start_slot = (exam_schedule.start_time.hour * 60 + exam_schedule.start_time.minute) 
            end_slot = (exam_schedule.end_time.hour * 60 + exam_schedule.end_time.minute) 
            
            time_slots = (
                db.query(ExamTimeSlot)
                .filter(
                    and_(
                        ExamTimeSlot.exam_date == exam_date,
                        ExamTimeSlot.time_slot >= start_slot,
                        ExamTimeSlot.time_slot <= end_slot
                    )
                )
                .with_for_update()
                .all()
            )
            
            if not time_slots:
                continue
                
            capacity_exceeded = any(slot.examinee_count + 1 > MAX_CAPACITY for slot in time_slots)
            
            if capacity_exceeded:
                reservation.reservation_status = "CANCEL"
                results["cancelled"] += 1
            else:
                reservation.reservation_status = "CONFIRM"
                for slot in time_slots:
                    slot.examinee_count += 1
                results["confirmed"] += 1
                
            db.add(reservation)
        except Exception as e:
            print(f"Error processing reservation {reservation.exam_reservations_id}: {str(e)}")
    
    db.commit()
    return results

def update_reservation_status(id: int, new_status: str, user_role: str, db: Session):
    if user_role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 예약 상태를 변경할 수 있습니다")
    
    reservation = db.query(ExamReservation).filter(ExamReservation.exam_reservations_id == id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약을 찾을 수 없습니다")
    
    if new_status not in ["PENDING", "CONFIRM", "CANCEL"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 예약 상태입니다")
    
    old_status = reservation.reservation_status
    
    if old_status == new_status:
        return reservation
    
    reservation.reservation_status = new_status
    
    if new_status == "CONFIRM" and old_status != "CONFIRM":
        update_time_slot_counts(reservation.exam_schedule_id, 1, db)
    elif old_status == "CONFIRM" and new_status != "CONFIRM":
        update_time_slot_counts(reservation.exam_schedule_id, -1, db)
    
    db.commit()
    db.refresh(reservation)
    return reservation