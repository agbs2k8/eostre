import asyncio
import sqlalchemy
import sqlalchemy.orm
from quart import Blueprint, jsonify, g, request
from src.services.auth_manager import auth_manager
from src.models.models import Account, User, Grant
import logging

logger = logging.getLogger(__name__)
account_user_bp = Blueprint("account_user_v1", __name__, url_prefix="/user")

@account_user_bp.route("/", methods=["GET"])
@auth_manager.jwt_required()
#@auth_manager.require_permissions("account.read")
async def get_account_users():
    account_id = g.user["account_id"]
    logger.info(f"User {g.user['sub']} retrieving the users for the account {account_id}")
    session = g.db_session
    result = await session.execute(
        sqlalchemy.select(User)
        .join(Grant, Grant.user_id == User.id)
        .where(Grant.account_id == account_id, 
                Grant.active == True,
                User.active == True,
                User.deleted == False)
        .options(
            sqlalchemy.orm.selectinload(User.email),
            sqlalchemy.orm.selectinload(User.grants)
                .selectinload(Grant.role)
        )   
    )
    users = result.scalars().unique().all()
    async def user_record(user: User):
        user_obj = {
            'id': user.id,
            'name': user.name,
            'type': user.type,
            'email': str(user.email),
            'created_date': user.created_date.isoformat(),
            'modified_date': user.modified_date.isoformat(),
            'grants': [await grant.to_dict() for grant in user.grants if grant.account_id == account_id]
        }
        return user_obj
    users_dict = [await user_record(user) for user in users]

    return jsonify(users_dict), 200