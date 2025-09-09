import jwt
from quart import Blueprint, request, jsonify, g
from quart_schema import validate_request, validate_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth_manager import auth_manager
from src.models.models import User
from src.services.schema import UserInput, RefreshTokenInput, AccountRequired

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


async def generate_user_payload(user: User, account_id: str, db_session: AsyncSession):
    permissions = await user.get_permissions(db_session)
    if account_id in permissions.keys():
        return {
            "sub": str(user.id),
            "username": user.name,
            "type": user.type,
            "account_id": account_id,
            "permissions": permissions
        }
    else:
        raise ValueError("User does not have permissions for the specified account")


@validate_request(UserInput)
@auth_bp.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    account_id = data.get("account")

    session = g.db_session
    if username: 
        user = await User.username_login(username, password, session)
    elif email:
        user = await User.email_login(email, password, session)
    else:
        return jsonify({"error": "Username or email is required"}), 400
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not account_id: 
        accounts = await user.get_authorized_accounts(session)
        if not accounts:
            return jsonify({"error": "No authorized accounts found"}), 403
        account_id = accounts[0].id  # TODO - something more sophisticated
    
    user_data = await generate_user_payload(user, account_id, session)
    access_token = auth_manager.create_access_token(user_data)
    refresh_token = auth_manager.create_refresh_token(user_data)

    response = jsonify({
        "access_token": access_token,
        "token_type": "Bearer"
    })

    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict", secure=True, path="/api/auth/refresh")

    return response


@validate_request(RefreshTokenInput)
@auth_bp.route("/refresh", methods=["POST"])
async def refresh_token():
    #token = (await request.get_json()).get("refresh_token")
    token = request.cookies.get("refresh_token")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        payload = auth_manager.verify_token(token)
        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError("Not a refresh token")
    except jwt.PyJWTError:
        return jsonify({"error": "Invalid or expired token"}), 401

    session = g.db_session
    user = await User.get(payload["sub"], session)
    
    user_data = await generate_user_payload(user, payload['account_id'], session)
    # New tokens (rotate refresh token)
    new_access_token = auth_manager.create_access_token(user_data)
    new_refresh_tooken = auth_manager.create_refresh_token(user_data)
    # Build response & set the cookie with the new refresh token
    response = jsonify({"access_token": new_access_token})
    response.set_cookie("refresh_token", new_refresh_tooken, httponly=True, samesite="Strict", secure=True, path="/api/auth/refresh")

    return response


@auth_bp.route("/switch_account", methods=["POST"])
@validate_request(AccountRequired)
@auth_manager.jwt_required()
async def switch_account():
    data = await request.get_json()
    session = g.db_session

    user = await User.get(g.user["sub"], session)
    if not user:
        return {"error": "User not found"}, 404

    # When gathering the user-data from that function, we pull the user permissions
    # from the database and ensure the account_id is in the keys of the permissions.
    user_data = await generate_user_payload(user, data.get("account_id"), session)
    new_token = auth_manager.create_access_token(user_data)

    return jsonify({"access_token": new_token})


@auth_bp.route("/logout", methods=["POST"])
async def logout():
    response = jsonify({"message": "Logout successful."})
    # Wipe out the refresh-token from the cookie
    response.set_cookie("refresh_token", "", httponly=True, secure=True, samesite="Strict", max_age=0)

    return response