# auth_middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime, timedelta, timezone

# Replace with your own secret key and algorithm
SECRET_KEY = "AIPLAYBOOK"
ALGORITHM = "HS256"


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bypass auth for login or public routes if needed
        if request.url.path in ["/auth/login", "/auth/register"]:
            return await call_next(request)

        # Extract token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
            )

        token = auth_header.split(" ")[1]

        try:
            # Decode the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Pass the user info to the request
        except JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
            )

        # Proceed with the request
        return await call_next(request)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt