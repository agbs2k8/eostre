from quart import jsonify
from . import api_v1_bp


@api_v1_bp.route('/liveness', methods=['GET'])
async def liveness():
    return jsonify({"message": "OK"}), 200


@api_v1_bp.route("/readiness", methods=['GET'])
async def readiness():
    return jsonify({"message": "OK"}), 200
