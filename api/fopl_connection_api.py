from flask import Blueprint, jsonify

fopl_connection_api = Blueprint(
    "fopl_connection_api",
    __name__,
    url_prefix="/api/fopl"
)

@fopl_connection_api.route("/connection", methods=["GET"])
def test_connection():
    return jsonify({
        "success": True,
        "project": "Friends of the Poway Library",
        "message": "Frontend successfully connected to Flask!",
        "status": "connected"
    }), 200