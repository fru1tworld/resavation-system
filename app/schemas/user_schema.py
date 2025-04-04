from pydantic import BaseModel

class UserCreateRequest(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }