"""
This module contains the routes for the reviews blueprint
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_reviews_from_place,
    get_reviews_from_user,
    get_review_by_id,
    get_reviews,
    update_review,
)

reviews_bp = Blueprint("reviews", __name__)

reviews_bp.route("/places/<place_id>/reviews", methods=["POST"])(jwt_required()(create_review))
reviews_bp.route("/places/<place_id>/reviews")(get_reviews_from_place)
reviews_bp.route("/users/<user_id>/reviews")(get_reviews_from_user)

reviews_bp.route("/reviews", methods=["GET"])(get_reviews)

reviews_bp.route("/reviews/<review_id>", methods=["GET"])(get_review_by_id)
reviews_bp.route("/reviews/<review_id>", methods=["PUT"])(jwt_required()(update_review))
reviews_bp.route("/reviews/<review_id>", methods=["DELETE"])(jwt_required()(delete_review))
