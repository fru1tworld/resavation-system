from pydantic import BaseModel

class ExamReservationCreateRequest(BaseModel):
    name: str
    descript: str
    max_capacity: int

class ExamReservationResponse(BaseModel):
    exam_reservation_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }