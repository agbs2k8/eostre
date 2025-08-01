from quart import Blueprint
from .account import account_bp
from .user import user_bp  # if you have a user.py

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Register individual endpoint blueprints under /api/v1
api_v1_bp.register_blueprint(account_bp)
api_v1_bp.register_blueprint(user_bp)