import jwt
import pathlib
import datetime
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Callable
from config import cfg


class TokenManager:
    def __init__(
        self,
        public_key: str,
        key_algorithm: str = "RS256",
    ):
        self.public_key = public_key
        self.key_algorithm = key_algorithm

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.public_key, algorithms=[self.key_algorithm])

    async def _get_token_from_request(self, request: Request) -> Optional[str]:
        # Check Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header.split(" ", 1)[1]

        # Check cookie
        token = request.cookies.get("access_token")
        if token:
            return token

        return None

    async def jwt_required(self, request: Request) -> dict:
        token = await self._get_token_from_request(request)

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token"
            )

        try:
            payload = self.verify_token(token)
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        request.state.user = payload  # Store user in request state
        return payload

    def require_permissions(self, *required_permissions):
        async def dependency(request: Request, user: dict = Depends(self.jwt_required)):
            current_account = user["account_id"]
            user_permissions = user["permissions"].get(str(current_account), [])

            if not any(p in user_permissions for p in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden - missing permissions"
                )
            return user

        return dependency


token_manager = TokenManager(
    public_key=cfg.PUBLIC_KEY if cfg.PUBLIC_KEY else pathlib.Path(cfg.PUBLIC_KEY_PATH).read_text(),
    key_algorithm=cfg.ENCRYPT_ALGORITHM
)
