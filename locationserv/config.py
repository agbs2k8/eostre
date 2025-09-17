from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
import uuid
import pathlib
import sys

class Settings(BaseSettings):
    APP_NAME: str = "locationserv"
    APP_VERSION: str = "0.0.1"
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", uuid.uuid4().hex)
    APP_URL: str = os.getenv("APP_URL", "http://127.0.0.1:5001")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG").upper()

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URI", "localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "microservice_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")

    # Token handling - paths only
    #PUBLIC_KEY_PATH: str = os.getenv("PUBLIC_KEY_PATH", "public_key.pem")
    # Public and Private Key Paths
    KEYS_DIR: str = pathlib.Path(os.getenv("KEYS_DIR", "../keys"))

    PUBLIC_KEY_PATH: str = pathlib.Path(
        os.getenv("PUBLIC_KEY_PATH", KEYS_DIR / "public_key.pem")
    )
    ENCRYPT_ALGORITHM: str = "RS256"
    def _read_required(path: pathlib.Path, name: str) -> str:
        if not path.exists():
            raise FileNotFoundError(
                f"{name} not found at {path}. "
                f"Set {name.upper()}_PATH or KEYS_DIR. Mounted keys dir contents: {list(KEYS_DIR.glob('*'))}"
            )
        return path.read_text(encoding="utf-8")

    PUBLIC_KEY: str = _read_required(PUBLIC_KEY_PATH, "public_key")

    LOG_CONFIG: dict = {}

    def model_post_init(self, __context):
        # Load key files at instance-level
        self.PUBLIC_KEY = pathlib.Path(self.PUBLIC_KEY_PATH).read_text()

        # Build logging config using the runtime LOG_LEVEL
        self.LOG_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "loggers": {
                "__main__": {
                    "level": self.LOG_LEVEL,
                    "handlers": ["console", "stderr"],
                    "propagate": False,
                },
                "uvicorn": {
                    "level": self.LOG_LEVEL,
                    "handlers": ["console"],
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": self.LOG_LEVEL,
                    "handlers": ["stderr"],
                    "propagate": False,
                },
                "uvicorn.access": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(process)d] [%(levelname)s] in %(module)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S %z",
                }
            },
            "handlers": {
                "stderr": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                    "formatter": "default",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                },
            },
            "root": {
                "level": self.LOG_LEVEL,
                "handlers": ["console", "stderr"]
            },
        }

cfg = Settings()
