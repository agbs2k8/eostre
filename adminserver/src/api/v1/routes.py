from quart import Blueprint, jsonify, g, request
from . import api_v1_bp
from src.services.auth_manager import auth_manager


@api_v1_bp.route('/liveness', methods=['GET'])
async def liveness():
    """
    Endpoint to check if the server is alive.
    """
    return jsonify({"message": "OK"}), 200


@api_v1_bp.route("/readiness", methods=['GET'])
async def readiness():
    return jsonify({"message": "OK"}), 200


@api_v1_bp.route("/hello-token", methods=["GET"])
@auth_manager.jwt_required()
#@auth_manager.require_roles(["admin"])
async def hello():
    token_content = auth_manager.verify_token(request.headers.get("Authorization").split(" ")[1])
    return jsonify({"message": f"Hello, {token_content['username']}!", "token": token_content}), 200


