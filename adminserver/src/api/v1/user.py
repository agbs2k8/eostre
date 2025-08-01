import sqlalchemy
from src.services.auth_manager import auth_manager
from src.models.models import User
from quart import Blueprint, jsonify, g, request
user_bp = Blueprint("user_v1", __name__, url_prefix="/user")


@user_bp.route('', methods=['GET'])
async def get_users():
    """
    Endpoint to retrieve all users.
    """
    session = g.db_session
    users = (await session.scalars(sqlalchemy.select(User))).all()
    user_dicts = [await user.to_dict() for user in users]
    return jsonify(user_dicts), 200


@user_bp.route("/me")
@auth_manager.jwt_required()
async def me():
    return jsonify({"user": g.user})