from pydantic import BaseModel
from datetime import datetime

class ExamScheduleCreateRequest(BaseModel):
    exam_info_id: int
    start_time: datetime
    end_time: datetime

class ExamScheduleResponse(BaseModel):
    exam_schedules_id: int
    exam_info_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime

    model_config = {
        'from_attributes': True
    }