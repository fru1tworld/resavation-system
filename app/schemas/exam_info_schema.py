from pydantic import BaseModel

class ExamInfoCreateRequest(BaseModel):
    name: str
    descript: str
    max_capacity: int

class ExamInfoResponse(BaseModel):
    exam_info_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }