from pydantic import BaseModel

class ExamScheduleCreateRequest(BaseModel):
    name: str
    descript: str
    max_capacity: int

class ExamScheduleResponse(BaseModel):
    user_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }