from quart import Blueprint
from .account_user import account_user_bp
from .account_base import account_v1_bp


# Register individual endpoint blueprints
account_v1_bp.register_blueprint(account_user_bp)