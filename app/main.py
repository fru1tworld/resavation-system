from fastapi import FastAPI
from app.routers.user_router import router as user_router
from app.routers.login_router import router as login_router
from app.routers.exam_info_router import router as exam_info_router
from app.routers.exam_categorie_router import router as exam_categorie_router
from app.routers.exam_reservation_router import router as exam_reservation_router
from app.routers.exam_schedules_router import router as exam_schedules_router
from app.middleware.auth_middleware import auth_middleware

app = FastAPI()

app.middleware("http")(auth_middleware)

app.include_router(user_router, prefix="/user")
app.include_router(login_router, prefix="/login")
app.include_router(exam_categorie_router, prefix="/exam-categorie")
app.include_router(exam_info_router, prefix="/exam-info")
app.include_router(exam_reservation_router, prefix="/exam-reservation")
app.include_router(exam_schedules_router, prefix="/exam-schedules")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
