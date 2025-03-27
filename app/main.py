from fastapi import FastAPI
from app.views.user_view import router as user_router
from app.views.login_view import router as login_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(login_router, prefix="/login")