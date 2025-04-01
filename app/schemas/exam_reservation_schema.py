from pydantic import BaseModel
from datetime import datetime

class ExamReservationCreateRequest(BaseModel):
    user_id: int
    exam_schedule_id: int

class ExamReservationResponse(BaseModel):
    exam_reservation_id: int
    user_id: int
    exam_schedule_id: int
    reservation_status: str
    created_at: datetime

    model_config = {
        'from_attributes': True
    }
