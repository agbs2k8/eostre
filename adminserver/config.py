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
SECURITY_PASSWORD_SALT = os.getenv("APP_PASSWORD_SALT", secrets.SystemRandom().getrandbits(128))
ENCRYPT_ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 10080
CORS_ORIGIN = (os.getenv("CORS_ORIGIN", "http://localhost:3000"))

# Email Sending Configs
SMTP_SERVER = os.getenv("SMTP_SERVER", "http://127.0.0.1")
SMTP_PORT = os.getenv("SMTP_PORT", 465)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "admin@test.dev")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "emailpassword")
EMAIL_ENABLED = bool(os.getenv("EMAIL_ENABLED", False))

# Handle Async vs Sync Database issues for Alembic
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite+aiosqlite:///adminserver.db")

if DATABASE_URI.startswith("sqlite+aiosqlite"):
    SYNC_DATABASE_URI = DATABASE_URI.replace("sqlite+aiosqlite", "sqlite", 1)
else:
    SYNC_DATABASE_URI = DATABASE_URI.replace("+asyncpg", "+psycopg2")  # for postgres

# Public and Private Key Paths
KEYS_DIR = pathlib.Path(os.getenv("KEYS_DIR", "keys"))

PRIVATE_KEY_PATH = pathlib.Path(
    os.getenv("PRIVATE_KEY_PATH", KEYS_DIR / "private_key.pem")
)
PUBLIC_KEY_PATH = pathlib.Path(
    os.getenv("PUBLIC_KEY_PATH", KEYS_DIR / "public_key.pem")
)

def _read_required(path: pathlib.Path, name: str) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"{name} not found at {path}. "
            f"Set {name.upper()}_PATH or KEYS_DIR. Mounted keys dir contents: {list(KEYS_DIR.glob('*'))}"
        )
    return path.read_text(encoding="utf-8")

PRIVATE_KEY = _read_required(PRIVATE_KEY_PATH, "private_key")
PUBLIC_KEY = _read_required(PUBLIC_KEY_PATH, "public_key")

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(process)d] [%(levelname)s] in %(module)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
            "formatter": "default",
        },
         "stderr": {
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
            "formatter": "default",
        }
    },
    "loggers": {
        "quart.app": {
            "level": LOG_LEVEL,
            "handlers": ["stdout"],
            "propagate": False,
        },
        "hypercorn.error": {
            "level": LOG_LEVEL,
            "handlers": ["stderr"],
            "propagate": False,
        },
        "hypercorn.access": {
            "level": LOG_LEVEL,
            "handlers": ["stdout"],
            "propagate": False,
        },
        "__main__": {
            "level": LOG_LEVEL,
            "handlers": ["stdout"],
            "propagate": False,
        },
    },
    "root": {"level": LOG_LEVEL, "handlers": ["stdout"]},
}