from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
import os

EXCLUDED_PATHS = ["/login", "/openapi.json", "/docs", "/redoc", "/health"]
GET_ONLY_EXCLUDED_PATHS = ["/exam-info", "/exam-categorie", "/exam-schedules"]
POST_ONLY_EXCLUDED_PATHS = ["/user", "/user/adm"]
ADMIN_PATHS = ["/adm"]

SECRET_KEY = os.getenv("SECRET_KEY", "happycat")
ALGORITHM = "HS256"

def is_excluded_path(path: str) -> bool:
    return any(path.startswith(item) for item in EXCLUDED_PATHS)

def is_get_excluded_path(method: str, path: str) -> bool:
    return method.upper() == "GET" and any(path.startswith(item) for item in GET_ONLY_EXCLUDED_PATHS)

def is_post_excluded_path(method: str, path: str) -> bool:
    return method.upper() == "POST" and any(path.startswith(item) for item in POST_ONLY_EXCLUDED_PATHS)

def is_admin_path(path: str) -> bool:
    return any(path.startswith(item) for item in ADMIN_PATHS)

async def auth_middleware(request: Request, call_next):
    if is_excluded_path(request.url.path):
        return await call_next(request)
    
    if is_get_excluded_path(request.method, request.url.path):
        return await call_next(request)
    
    if is_post_excluded_path(request.method, request.url.path):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401, 
            content={"detail": "인증이 필요합니다. 유효한 Bearer 토큰을 제공하세요."}
        )
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_role = payload.get("role", "USER")
        
        if not username:
            return JSONResponse(status_code=401, content={"detail": "유효하지 않은 토큰입니다."})
        
        if is_admin_path(request.url.path) and user_role != "ADMIN":
            return JSONResponse(
                status_code=403, 
                content={"detail": "관리자 권한이 필요합니다."}
            )
        
        request.state.user_name = username
        request.state.user_role = user_role
        
        response = await call_next(request)
        return response
        
    except JWTError:
        return JSONResponse(status_code=401, content={"detail": "유효하지 않은 토큰입니다."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
