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
    KEYS_DIR: str = pathlib.Path(os.getenv("KEYS_DIR", "../keys"))
    PUBLIC_KEY_PATH: str = pathlib.Path(
        os.getenv("PUBLIC_KEY_PATH", KEYS_DIR / "public_key.pem")
    )
    ENCRYPT_ALGORITHM: str = "RS256"
    PUBLIC_KEY: str = pathlib.Path(PUBLIC_KEY_PATH).read_text()
    LOG_JSON: bool = os.getenv("LOG_JSON", "false").lower() == "true"
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
        base_formatter = {
            "format": "[%(asctime)s] [%(process)d] [%(levelname)s] in %(module)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        }
        json_formatter = {
            "format": '{"ts":"%(asctime)s","lvl":"%(levelname)s","logger":"%(name)s",'
                      '"module":"%(module)s","user":"%(user_id)s","msg":"%(message)s"}',
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        }
        log_format = json_formatter if self.LOG_JSON else base_formatter
        self.LOG_CONFIG["formatters"]["default"] = log_format

cfg = Settings()
