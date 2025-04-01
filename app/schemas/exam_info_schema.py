from pydantic import BaseModel
from datetime import datetime

class ExamInfoCreateRequest(BaseModel):
    exam_name: str
    exam_description: str
    exam_category_id: int

class ExamInfoResponse(BaseModel):
    exam_info_id: int
    exam_name: str
    exam_description: str
    exam_category_id: int
    created_at: datetime

    model_config = {
        'from_attributes': True
    }