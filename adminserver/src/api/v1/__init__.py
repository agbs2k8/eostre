from quart import Blueprint
from .account import account_v1_bp
from .user import user_bp 
from .grants import grants_bp
from .roles import roles_bp
from .email import email_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Register individual endpoint blueprints under /api/v1
api_v1_bp.register_blueprint(account_v1_bp)
api_v1_bp.register_blueprint(user_bp)
api_v1_bp.register_blueprint(grants_bp)  
api_v1_bp.register_blueprint(roles_bp)
api_v1_bp.register_blueprint(email_bp)
