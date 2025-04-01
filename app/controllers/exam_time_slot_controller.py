from sqlalchemy.orm import Session
from app.models.exam_time_slot import ExamTimeSlot
from datetime import datetime, timedelta
from app.models.exam_schedule import ExamSchedule

MAX_CAPACITY = 50000

def create_exam_time_slots(schedule_id: int, db: Session):
    schedule = db.query(ExamSchedule).where(ExamSchedule.exam_schedule_id == schedule_id).first()
    if not schedule:
        return {"error": "시험 스케줄을 찾을 수 없습니다"}
    
    start_time = schedule.start_time
    end_time = schedule.end_time
    
    current_time = start_time
    slots_created = 0
    
    while current_time < end_time:
        time_slot_value = current_time.hour * 60 + current_time.minute
        
        exists = db.query(ExamTimeSlot).where(
            ExamTimeSlot.exam_date == current_time.date(),
            ExamTimeSlot.time_slot == time_slot_value
        ).first()
        
        if not exists:
            new_slot = ExamTimeSlot(
                exam_date=current_time.date(),
                time_slot=time_slot_value,
                confirm_count=0  
            )
            db.add(new_slot)
            slots_created += 1
        
        current_time += timedelta(minutes=30)
    
    db.commit()
    return {"message": f"{slots_created}개의 시간 슬롯이 생성되었습니다."}

def get_time_slot_availability(date: datetime.date, db: Session):
    slots = db.query(ExamTimeSlot).where(ExamTimeSlot.exam_date == date).all()
    
    availability = []
    for slot in slots:
        time_str = f"{slot.time_slot // 60:02d}:{slot.time_slot % 60:02d}"
        availability.append({
            "time": time_str,
            "confirm_count": slot.confirm_count,
            "available": slot.confirm_count < MAX_CAPACITY
        })
    
    return availability