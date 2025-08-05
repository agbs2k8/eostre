import asyncio
import sqlalchemy
import sqlalchemy.orm
from src.services.auth_manager import auth_manager
from src.models.models import User, Grant, Role#, account_user_table
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
    
    result = await session.execute(
        sqlalchemy.select(User)
        .where(User.active == True,
               User.deleted == False,
               User.id.in_(
                   sqlalchemy.select(Grant.user_id).where(
                       Grant.account_id == account_id,
                       Grant.active == True)))
        .options(
            sqlalchemy.orm.selectinload(User.email),
            sqlalchemy.orm.selectinload(User.alternate_emails),
            sqlalchemy.orm.selectinload(User.grants)
                .selectinload(Grant.role)
                .selectinload(Role.permissions),
            sqlalchemy.orm.selectinload(User.grants)
                .selectinload(Grant.account),
        )
    )
    users = result.scalars().all()

    # Wrap in a function for now...
    async def full_user_record(user: User):
        user_obj = {
            'id': user.id,
            'name': user.name,
            'type': user.type,
            'email': str(user.email),
            'alternate_emails': [str(email) for email in user.alternate_emails],
            'personal_name': user.personal_name,
            'family_names': user.family_names,
            'display_name': user.display_name,
            'active': user.active,
            'created_date': user.created_date.isoformat(),
            'modified_date': user.modified_date.isoformat(),
            'deleted': user.deleted,
            'grants': await asyncio.gather(*(grant.to_dict() for grant in user.grants)),
            'permissions': await user.get_permissions(session)
        }

        return user_obj
    user_dicts = [await full_user_record(user) for user in users]
    return jsonify(user_dicts), 200


@user_bp.route('/', methods=['POST'])
@auth_manager.jwt_required()
async def add_user():
    # TODO - update other uses on the account
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
    logger.info(f"User {g.user['sub']} their personal record")
    return jsonify({"user": g.user})


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

