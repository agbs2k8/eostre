import asyncio
import sqlalchemy
import sqlalchemy.orm
from src.services.auth_manager import auth_manager
from src.models.models import User, Grant, Role, Email#, account_user_table
from quart import Blueprint, jsonify, g, request
import logging

logger = logging.getLogger(__name__)
user_bp = Blueprint("user_v1", __name__, url_prefix="/user")


@user_bp.route('', methods=['GET'])
@auth_manager.jwt_required()
async def get_users():
    """
    Endpoint to retrieve all users for the current account.
    """
    session = g.db_session
    account_id = g.user["account_id"]
    logger.info(f"User {g.user['sub']} Retrieving users for account {account_id}")
    user_dicts = await User.get_all_json_by_account(account_id, g.db_session)
    return jsonify(user_dicts), 200


@user_bp.route('/', methods=['POST'])
@auth_manager.jwt_required()
async def add_user():
    """
    Add a new user to the current account.
    """
    session = g.db_session
    account_id = g.user["account_id"]
    logger.info(f"User {g.user['sub']} Adding user for account {account_id}")
    
    # TODO - add user on the account
    return jsonify({"message": "ok"}), 200


@user_bp.route('/', methods=['PUT'])
@auth_manager.jwt_required()
async def update_user():
    # TODO - update other uses on the account
    return jsonify({"message": "ok"}), 200


@user_bp.route('/', methods=['DELETE'])
@auth_manager.jwt_required()
async def remove_user():
    # TODO - remove the user from the account
    return jsonify({"message": "ok"}), 200


@user_bp.route("/me", methods=['GET'])
@auth_manager.jwt_required()
async def get_me():
    """
    Retrieve all of the pertinent data for the current user
    """
    async with g.db_session as session:
        user_id = g.user["sub"]
        logger.info(f"User {user_id} accessing their personal record")

        user = await User.get_json_user_by_id(user_id, session)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200


@user_bp.route("/me", methods=['PUT'])
@auth_manager.jwt_required()
async def update_me():
    # TODO
    logger.info(f"User {g.user['sub']} their personal record")
    return jsonify({"user": g.user})


@user_bp.route("/me", methods=['PUT'])
@auth_manager.jwt_required()
async def delete_me():
    # TODO
    logger.info(f"User {g.user['sub']} their personal record")
    return jsonify({"user": g.user})


@user_bp.route('/authorized_accounts', methods=['GET'])
@auth_manager.jwt_required()
async def authorized_accounts():
    """
    Endpoint to retrieve accounts the user is authorized to access.
    """
    logger.info(f"User {g.user['sub']} retrieving their authorized accounts")
    session = g.db_session
    user = await User.get(g.user.get('sub'), session)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    accounts = await user.get_authorized_accounts(session)
    account_dicts = await asyncio.gather(*(account.to_dict() for account in accounts))
    return jsonify(account_dicts), 200

