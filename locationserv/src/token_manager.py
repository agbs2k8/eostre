import jwt
import pathlib
import logging
from fastapi import Request, HTTPException, status, Depends
from typing import Optional
from config import cfg

logger = logging.getLogger("locationserv.auth")


class TokenManager:
    def __init__(self, public_key: str, key_algorithm: str = "RS256"):
        self.public_key = public_key
        self.key_algorithm = key_algorithm

    def verify_token(self, token: str) -> dict:
        kwargs = {}
        if getattr(cfg, "TOKEN_AUDIENCE", ""):
            kwargs["audience"] = cfg.TOKEN_AUDIENCE
        if getattr(cfg, "TOKEN_ISSUER", ""):
            kwargs["issuer"] = cfg.TOKEN_ISSUER
        return jwt.decode(token, self.public_key, algorithms=[self.key_algorithm], **kwargs)

    async def _get_token_from_request(self, request: Request) -> Optional[str]:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header.split(" ", 1)[1].strip()
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            return cookie_token.strip()
        return None

    async def jwt_required(self, request: Request) -> dict:
        token = await self._get_token_from_request(request)
        if not token:
            logger.debug("auth_missing_token path=%s", request.url.path)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
        try:
            payload = self.verify_token(token)
        except jwt.ExpiredSignatureError:
            logger.info("auth_expired path=%s", request.url.path)
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        except jwt.InvalidAudienceError:
            logger.info("auth_invalid_audience path=%s token_aud_claim", request.url.path)
            raise HTTPException(status_code=401, detail="Invalid audience")
        except jwt.InvalidIssuerError:
            logger.info("auth_invalid_issuer path=%s", request.url.path)
            raise HTTPException(status_code=401, detail="Invalid issuer")
        except jwt.ImmatureSignatureError:
            logger.info("auth_immature_token path=%s", request.url.path)
            raise HTTPException(status_code=401, detail="Token not yet valid")
        except jwt.DecodeError:
            logger.info("auth_decode_error path=%s", request.url.path)
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        except jwt.PyJWTError as exc:
            logger.info("auth_other_jwt_error=%s path=%s", type(exc).__name__, request.url.path)
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        request.state.user = payload
        return payload

    def require_permissions(self, *required_permissions: str):
        async def dependency(request: Request, user: dict = Depends(self.jwt_required)):
            account_id = user.get("account_id")
            permissions_map = user.get("permissions") or {}
            # Expect permissions keyed by account_id string
            user_perms = permissions_map.get(str(account_id), [])
            if not any(p in user_perms for p in required_permissions):
                # 403: authenticated but insufficient rights
                raise HTTPException(status_code=403, detail="Forbidden - missing permissions")
            return user
        return dependency


token_manager = TokenManager(
    public_key=cfg.PUBLIC_KEY if cfg.PUBLIC_KEY else pathlib.Path(cfg.PUBLIC_KEY_PATH).read_text(),
    key_algorithm=cfg.ENCRYPT_ALGORITHM
)
