import asyncio
import sqlalchemy
import sqlalchemy.orm
from quart import Blueprint, jsonify, g, request
from src.services.auth_manager import auth_manager
from src.models.models import Account, User, Grant
import logging

logger = logging.getLogger(__name__)
account_v1_bp = Blueprint("account_v1", __name__, url_prefix="/account")

@account_v1_bp.route("", methods=["GET"])
@auth_manager.jwt_required()
@auth_manager.require_permissions("account.read")
async def get_account():
    account_id = g.user["account_id"]
    logger.info(f"User {g.user['sub']} retrieving the account details for account {account_id}")
    session = g.db_session
    account = await Account.get(account_id, session)
    if not account:
        return jsonify({"error": "Not found"}), 404
    account_dict = await account.to_dict()
    return jsonify(account_dict), 200


@account_v1_bp.route("", methods=["POST"])
@auth_manager.jwt_required()
@auth_manager.require_permissions("account.write")
async def create_account():
    data = await request.get_json()
    # Create a new account
    # THIS NEEDS TO ENTAIL - Create new account, add account.read & account.write permissions to the current system user
    return jsonify({"action": "create", "data": data}), 201


@account_v1_bp.route("", methods=["PUT"])
async def update_account():
    data = await request.get_json()
    # Update account
    return jsonify({"action": "update", "data": data})


@account_v1_bp.route("", methods=["DELETE"])
async def delete_account():
    # Delete account
    return jsonify({"action": "delete"})

