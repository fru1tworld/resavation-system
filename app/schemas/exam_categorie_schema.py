from pydantic import BaseModel

class ExamCategorieCreateRequest(BaseModel):
    name: str
    descript: str
    max_capacity: int

class ExamCategorieResponse(BaseModel):
    exam_categorie_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }