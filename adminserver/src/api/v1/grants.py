from quart import Blueprint, jsonify, g, request
from src.services.auth_manager import auth_manager
import logging

logger = logging.getLogger(__name__)
grants_bp = Blueprint("grants_v1", __name__, url_prefix="/grant")


@grants_bp.route("", methods=["POST"])
async def grant_role():
    data = await request.get_json()
    # Create a new account
    return jsonify({"action": "create", "data": data}), 201


@grants_bp.route("", methods=["PUT"])
async def update_grant():
    data = await request.get_json()
    # Update account
    return jsonify({"action": "update", "data": data})


@grants_bp.route("", methods=["DELETE"])
async def revoke_grant():
    # Delete account
    return jsonify({"action": "delete"})