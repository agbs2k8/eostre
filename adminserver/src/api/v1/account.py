from quart import Blueprint, jsonify, g, request
account_bp = Blueprint("account_v1", __name__, url_prefix="/account")

@account_bp.route("", methods=["GET"])
async def get_account():
    # Return account(s)
    return jsonify({"action": "get"})


@account_bp.route("", methods=["POST"])
async def create_account():
    data = await request.get_json()
    # Create a new account
    return jsonify({"action": "create", "data": data}), 201


@account_bp.route("", methods=["PUT"])
async def update_account():
    data = await request.get_json()
    # Update account
    return jsonify({"action": "update", "data": data})


@account_bp.route("", methods=["DELETE"])
async def delete_account():
    # Delete account
    return jsonify({"action": "delete"})
