import os
import sys
import uuid
import secrets
import pathlib

APP_NAME = "adminserver"
APP_VERSION = "0.0.1"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", uuid.uuid4().hex)
APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite+aiosqlite:///adminserver.db")
SECURITY_PASSWORD_SALT = os.getenv("APP_PASSWORD_SALT", secrets.SystemRandom().getrandbits(128))
ENCRYPT_ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 10080

# Public and Private Key Paths
PRIVATE_KEY = pathlib.Path(os.getenv("PRIVATE_KEY_PATH", "private_key.pem")).read_text()
PUBLIC_KEY = pathlib.Path(os.getenv("PUBLIC_KEY_PATH", "public_key.pem")).read_text()

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        # "flask.app": {
        #     "level": "ERROR",
        #     "handlers": ["wsgi"],
        #     "propagate": False,
        # },
         "quart.app": {  
            "level": LOG_LEVEL,
            "handlers": ["console","wsgi"],
            "propagate": False,
        },
        "__main__": { 
            "level": LOG_LEVEL,
            "handlers": ["console", "wsgi"],
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
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
         "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "default",
        }
    },
    "root": {"level": LOG_LEVEL, "handlers": ["console", "wsgi"]},
}