import sqlalchemy
import sqlalchemy.orm
from quart import Blueprint, jsonify, g, request
from src.services.auth_manager import auth_manager
from src.models.models import Role
import logging

logger = logging.getLogger(__name__)
roles_bp = Blueprint("roles_v1", __name__, url_prefix="/role")


@roles_bp.route("", methods=["GET"])
@auth_manager.jwt_required()
async def get_roles():
    session = g.db_session
    #account_id = g.user["account_id"]
    logger.info(f"User {g.user['sub']} Retrieving roles list.")
    
    result = await session.execute(
        sqlalchemy.select(Role)
        .where(Role.active == True, Role.deleted == False)
        .options(
            sqlalchemy.orm.selectinload(Role.permissions)
        )
    )
    roles = result.scalars().all()
    role_dicts = [await role.to_dict() for role in roles]
    return jsonify(role_dicts), 200

@roles_bp.route("", methods=["POST"])
async def create_role():
    data = await request.get_json()
    # Create a new role
    return jsonify({"action": "create", "data": data}), 201


@roles_bp.route("", methods=["PUT"])
async def update_role():
    data = await request.get_json()
    # Update role
    return jsonify({"action": "update", "data": data})


@roles_bp.route("", methods=["DELETE"])
async def delete_role():
    # Delete role
    return jsonify({"action": "delete"})