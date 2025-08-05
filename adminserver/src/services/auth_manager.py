import jwt
import datetime
from functools import wraps
from quart import request, jsonify, g
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
import config as cfg


class AuthManager:
    def __init__(
        self, 
        private_key,
        public_key,
        access_token_expiry=15, 
        refresh_token_expiry=1440,
        key_algorithm="RS256"
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.access_token_expiry = access_token_expiry
        self.refresh_token_expiry = refresh_token_expiry
        self.key_algorithm = key_algorithm

    def _build_payload(self, data: dict, minutes: int, token_type: str):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        return {
            **data,
            "type": token_type,
            "iat": now,
            "exp": now + datetime.timedelta(minutes=minutes)
        }

    def create_access_token(self, data: dict) -> str:
        payload = self._build_payload(data, self.access_token_expiry, "access")
        return jwt.encode(payload, self.private_key, algorithm=self.key_algorithm)

    def create_refresh_token(self, data: dict) -> str:
        payload = self._build_payload(data, self.refresh_token_expiry, "refresh")
        return jwt.encode(payload, self.private_key, algorithm=self.key_algorithm)

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.public_key, algorithms=[self.key_algorithm])

    def jwt_required(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                auth_header = request.headers.get("Authorization", "")
                token = None
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ", 1)[1]
                elif "access_token" in request.cookies:
                    token = request.cookies["access_token"]

                if not token:
                    return {"error": "Missing token"}, 401

                try:
                    payload = self.verify_token(token)
                    g.user = payload
                except jwt.PyJWTError:
                    return {"error": "Invalid or expired token"}, 401

                return await func(*args, **kwargs)
            return wrapper
        return decorator

    def require_permissions(self, *required_permissions):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                current_account = g.user["account_id"]
                user_permissions = g.user["permissions"].get(str(current_account))
                if not any(permission in user_permissions for permission in required_permissions):
                    return {"error": "Forbidden - missing permissions"}, 403
                return await func(*args, **kwargs)
            return wrapper
        return decorator

auth_manager = AuthManager(
    private_key=cfg.PRIVATE_KEY,
    public_key=cfg.PUBLIC_KEY,
    access_token_expiry=cfg.ACCESS_TOKEN_EXPIRE_MINUTES,
    refresh_token_expiry=cfg.REFRESH_TOKEN_EXPIRE_MINUTES,
    key_algorithm=cfg.ENCRYPT_ALGORITHM
)