import jwt
from quart import Blueprint, request, jsonify, g
from quart_schema import validate_request, validate_response
from src.services.auth_manager import auth_manager
from src.models.models import User
from src.services.schema import UserInput

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@validate_request(UserInput)
@auth_bp.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    username = data.get("username")
    password = data.get("password")

    session = g.db_session
    user = await User.login(username, password, session)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    user_data = {
        "sub": str(user.id),
        "username": user.name,
        "type": user.type
    }

    access_token = auth_manager.create_access_token(user_data)
    refresh_token = auth_manager.create_refresh_token(user_data)

    response = jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    })

    response.set_cookie("access_token", access_token, httponly=True, samesite="Strict", secure=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict", secure=True)

    return response


@auth_bp.route("/refresh", methods=["POST"])
async def refresh_token():
    token = (await request.get_json()).get("refresh_token")

    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = auth_manager.verify_token(token)
        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError("Not a refresh token")
    except jwt.PyJWTError:
        return jsonify({"error": "Invalid or expired token"}), 401

    # NOTE: Do not re-issue refresh token unless you're rotating them
    new_access_token = auth_manager.create_access_token({
        "sub": payload["sub"],
        "username": payload["username"],
        "type": payload["type"]
    })

    response = jsonify({"access_token": new_access_token})
    response.set_cookie("access_token", new_access_token, httponly=True, samesite="Strict", secure=True)

    return response
