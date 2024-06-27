from src.models.base import Base
from src import db
from src.models.user import User
from src.models.city import City
from flask_jwt_extended import get_jwt_identity


class Place(Base):
    """Place representation"""

    __tablename__ = 'places'

    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    def __init__(self, data: dict | None = None, **kw) -> None:
        """Initialize a Place instance"""
        super().__init__(**kw)

        if data:
            self.name = data.get("name", "")
            self.description = data.get("description", "")
            self.address = data.get("address", "")
            self.latitude = float(data.get("latitude", 0.0))
            self.longitude = float(data.get("longitude", 0.0))
            self.host_id = self.get_current_user_id()
            self.city_id = data["city_id"]
            self.price_per_night = int(data.get("price_per_night", 0))
            self.number_of_rooms = int(data.get("number_of_rooms", 0))
            self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
            self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        """String representation of Place"""
        return f"<Place {self.id} ({self.name})>"
    
    @staticmethod
    def get_current_user_id():
        """Get the current user's ID from JWT"""
        return get_jwt_identity().get('id')


    def to_dict(self) -> dict:
        """Return dictionary representation of Place"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "host_id": self.host_id,
            "city_id": self.city_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        from src.persistence import repo

        user: User | None = User.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city: City | None = City.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)
        repo.save(new_place)

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        from src.persistence import repo

        place: Place | None = Place.get(place_id)
        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        repo.update(place)

        return place

    @classmethod
    def get(cls, place_id: str) -> "Place | None":
        """Get a place by ID"""
        from src.persistence import repo

        return repo.get(cls.__name__.lower(), place_id)

    @classmethod
    def get_all(cls) -> list["Place"]:
        """Get all places"""
        from src.persistence import repo

        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, place_id: str) -> bool:
        """Delete a place by ID"""
        from src.persistence import repo

        place = cls.get(place_id)
        if not place:
            return False

        return repo.delete(place)
