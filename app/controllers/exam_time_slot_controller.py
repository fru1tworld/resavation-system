from sqlalchemy.orm import Session
from app.models.exam_time_slot import ExamTimeSlot
from datetime import datetime, timedelta, timezone
from app.models.exam_schedule import ExamSchedule
from fastapi import HTTPException, status
from app.utils.snowflake import generate_snowflake_id

MAX_CAPACITY = 50000

def create_exam_time_slots(schedule_id: int, db: Session):
    schedule = db.query(ExamSchedule).filter(ExamSchedule.exam_schedules_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="시험 스케줄을 찾을 수 없습니다")
    
    start_time = schedule.start_time
    end_time = schedule.end_time
    
    current_time = start_time
    slots_created = 0
    
    while current_time < end_time:
        time_slot_value = current_time.hour * 60 + current_time.minute
        
        exists = db.query(ExamTimeSlot).filter(
            ExamTimeSlot.exam_date == current_time.date(),
            ExamTimeSlot.time_slot == time_slot_value
        ).first()
        
        if not exists:
            new_slot = ExamTimeSlot(
                exam_time_slot_id=generate_snowflake_id(),
                exam_date=current_time.date(),
                time_slot=time_slot_value,
                examinee_count=0,
                created_at=datetime.now(timezone.utc)
            )
            db.add(new_slot)
            slots_created += 1
        
        current_time += timedelta(minutes=30)
    
    db.commit()
    return {"message": f"{slots_created}개의 시간 슬롯이 생성되었습니다."}

def get_time_slot_availability(date: datetime.date, db: Session):
    slots = db.query(ExamTimeSlot).filter(ExamTimeSlot.exam_date == date).all()
    
    if not slots:
        return []
        
    availability = []
    for slot in slots:
        time_str = f"{slot.time_slot // 60:02d}:{slot.time_slot % 60:02d}"
        availability.append({
            "time": time_str,
            "examinee_count": slot.examinee_count,
            "available": slot.examinee_count < MAX_CAPACITY
        })
    
    return availability