from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str

class UserRead(BaseModel):
    user_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }
