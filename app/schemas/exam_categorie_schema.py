from pydantic import BaseModel
from datetime import datetime

class ExamCategorieCreateRequest(BaseModel):
    name: str

class ExamCategorieResponse(BaseModel):
    exam_categorie_id: int
    name: str
    created_at: datetime

    model_config = {
        'from_attributes': True
    }