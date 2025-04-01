from pydantic import BaseModel
from app.schemas.user_schema import UserResponse

class LoginForm(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    is_admin: bool