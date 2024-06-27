"""
This module contains the routes for the amenities blueprint.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.amenities import (
    create_amenity,
    delete_amenity,
    get_amenity_by_id,
    get_amenities,
    update_amenity,
)

amenities_bp = Blueprint("amenities", __name__, url_prefix="/amenities")

amenities_bp.route("/", methods=["GET"])(get_amenities)
amenities_bp.route("/", methods=["POST"])(jwt_required()(create_amenity))

amenities_bp.route("/<amenity_id>", methods=["GET"])(get_amenity_by_id)
amenities_bp.route("/<amenity_id>", methods=["PUT"])(jwt_required()(update_amenity))
amenities_bp.route("/<amenity_id>", methods=["DELETE"])(jwt_required()(delete_amenity))
