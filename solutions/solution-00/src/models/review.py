from src.models.base import Base
from src import db
from src.models.place import Place
from src.models.user import User
from typing import Optional


class Review(Base):
    """Review representation"""

    __tablename__ = 'reviews'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, place_id: str, user_id: str, comment: str, rating: float, **kw):
        """Initialize a Review instance"""
        super().__init__(**kw)

        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        """String representation of Review"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Return dictionary representation of Review"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        from src.persistence import repo

        user: User | None = User.get(data["user_id"])
        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place: Place | None = Place.get(data["place_id"])
        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        repo.save(new_review)

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        from src.persistence import repo

        review: Review | None = Review.get(review_id)
        if not review:
            return None

        for key, value in data.items():
            setattr(review, key, value)

        repo.update(review)

        return review

    @classmethod
    def get(cls, review_id: str) -> "Review | None":
        """Get a review by ID"""
        from src.persistence import repo

        return repo.get(cls.__name__.lower(), review_id)

    @classmethod
    def get_all(cls) -> list["Review"]:
        """Get all reviews"""
        from src.persistence import repo

        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, review_id: str) -> bool:
        """Delete a review by ID"""
        from src.persistence import repo

        review = cls.get(review_id)
        if not review:
            return False

        return repo.delete(review)
