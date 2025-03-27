from pydantic import BaseModel

class LoginForm(BaseModel):
    name: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    name: str
    role: str

    model_config = {
        'from_attributes': True
    }