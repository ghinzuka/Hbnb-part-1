"""
This module contains the routes for the places blueprint
"""

from flask import jsonify
from flask import Blueprint
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)
from flask_jwt_extended import jwt_required, get_jwt_identity

places_bp = Blueprint("places", __name__, url_prefix="/places")

places_bp.route("/", methods=["GET"])(get_places)
places_bp.route("/", methods=["POST"])(jwt_required()(create_place))

places_bp.route("/<place_id>", methods=["GET"])(get_place_by_id)
places_bp.route("/<place_id>", methods=["PUT"])(jwt_required()(update_place))
places_bp.route("/<place_id>", methods=["DELETE"])(jwt_required()(delete_place))

# Example of a protected route to demonstrate JWT usage
@places_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200