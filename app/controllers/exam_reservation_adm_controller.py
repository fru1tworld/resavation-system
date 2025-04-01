from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.exam_reservation import ExamReservation
from app.models.exam_time_slot import ExamTimeSlot  
from app.models.exam_schedule import ExamSchedule  

MAX_CAPACITY = 50000

def confirm_reservations_batch(db: Session):
    pending_reservations = (
        db.query(ExamReservation)
        .where(ExamReservation.status == "PENDING")
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
                .where(ExamSchedule.exam_schedule_id == reservation.exam_schedule_id)
                .first()
            )
            if not exam_schedule:
                continue
            
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
            
            capacity_exceeded = any(slot.confirm_count + 1 > MAX_CAPACITY for slot in time_slots)
            
            if capacity_exceeded:
                reservation.status = "CANCEL"
                results["cancelled"] += 1
            else:
                reservation.status = "CONFIRM"
                for slot in time_slots:
                    slot.confirm_count += 1
                results["confirmed"] += 1
                
            db.add(reservation)
        except Exception as e:
            print(f"Error processing reservation {reservation.test_reservation_id}: {str(e)}")
    
    db.commit()
    return results

def update_reservation_status(id: int, new_status: str, user_role: str, db: Session):
    if user_role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 예약 상태를 변경할 수 있습니다")
    
    reservation = db.query(ExamReservation).where(ExamReservation.exam_reservation_id == id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약을 찾을 수 없습니다")
    
    old_status = reservation.status
    reservation.status = new_status
    
    if new_status == "CONFIRM" and old_status != "CONFIRM":
        update_time_slot_counts(reservation.exam_schedule_id, 1, db)

    elif old_status == "CONFIRM" and new_status != "CONFIRM":
        update_time_slot_counts(reservation.exam_schedule_id, -1, db)
    
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