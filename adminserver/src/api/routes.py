from quart import Blueprint, jsonify, g, request
import sqlalchemy
from src.services.auth_manager import auth_manager
from src.models.models import User

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/v1/me")
@auth_manager.jwt_required()
async def me():
    return jsonify({"user": g.user})


@api_bp.route('/v1/liveness', methods=['GET'])
async def liveness():
    """
    Endpoint to check if the server is alive.
    """
    return jsonify({"message": "OK"}), 200


@api_bp.route("/v1/readiness", methods=['GET'])
async def readiness():
    return jsonify({"message": "OK"}), 200


@api_bp.route('/v1/users', methods=['GET'])
async def get_users():
    """
    Endpoint to retrieve all users.
    """
    session = g.db_session
    users = (await session.scalars(sqlalchemy.select(User))).all()
    user_dicts = [await user.to_dict() for user in users]
    return jsonify(user_dicts), 200


@api_bp.route("/v1/hello-token", methods=["GET"])
@auth_manager.jwt_required()
#@auth_manager.require_roles(["admin"])
async def hello():
    token_content = auth_manager.verify_token(request.headers.get("Authorization").split(" ")[1])
    return jsonify({"message": f"Hello, {token_content['username']}!", "token": token_content}), 200
