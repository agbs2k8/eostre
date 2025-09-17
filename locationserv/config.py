import os
import uuid
import sys
import logging
import hashlib
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Any, Dict
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "locationserv"
    APP_VERSION: str = "0.0.1"
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", uuid.uuid4().hex)
    APP_URL: str = os.getenv("APP_URL", "http://127.0.0.1:5001")
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG").upper()
    LOG_JSON: bool = os.getenv("LOG_JSON", "false").lower() == "true"
    
    # Keys
    KEYS_DIR: Path = Path(os.getenv("KEYS_DIR", "/app/keys"))
    PUBLIC_KEY_PATH: Path = Field(default_factory=lambda: Path(os.getenv("PUBLIC_KEY_PATH", "/app/keys/public_key.pem")))
    ENCRYPT_ALGORITHM: str = os.getenv("ENCRYPT_ALGORITHM", "RS256")

    # Database (raw values only; no secrets in logs)
    DATABASE_URL: str = os.getenv("DATABASE_URI", "localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "microservice_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")

    # Populated at runtime
    PUBLIC_KEY: str = ""
    LOG_CONFIG: Dict[str, Any] = {}

    def model_post_init(self, __context: Any) -> None:
        # Load public key file (do not expose full key in logs)
        try:
            self.PUBLIC_KEY = self.PUBLIC_KEY_PATH.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise RuntimeError(f"Public key not found at {self.PUBLIC_KEY_PATH}")
        fp = hashlib.sha256(self.PUBLIC_KEY.encode("utf-8")).hexdigest()[:32]

        self.LOG_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": (
                        '{"ts":"%(asctime)s","lvl":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
                        if self.LOG_JSON else
                        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
                    ),
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                }
            },
            "root": {
                "level": self.LOG_LEVEL,
                "handlers": ["console"],
            },
        }

        logging.basicConfig(level=self.LOG_LEVEL)
        logging.getLogger("locationserv.startup").info(
            "Loaded public key fingerprint=%s path=%s", fp, self.PUBLIC_KEY_PATH
        )

cfg = Settings()
