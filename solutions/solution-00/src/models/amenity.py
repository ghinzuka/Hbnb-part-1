from src.models.base import Base
from src import db
from typing import Optional

class Amenity(Base):
    """Amenity representation"""

    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name: str, **kw) -> None:
        """Initialize an Amenity instance"""
        super().__init__(**kw)
        self.name = name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        new_amenity = Amenity(**data)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None
        for key, value in data.items():
            setattr(amenity, key, value)
        db.session.commit()
        return amenity


    @classmethod
    def get(cls, amenity_id: str) -> Optional["Amenity"]:
        """Get an amenity by ID"""
        from src.persistence import repo

        return repo.get(cls.__name__.lower(), amenity_id)

    @classmethod
    def get_all(cls) -> list["Amenity"]:
        """Get all amenities"""
        from src.persistence import repo

        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, amenity_id: str) -> bool:
        """Delete an amenity by ID"""
        from src.persistence import repo

        amenity = cls.get(amenity_id)
        if not amenity:
            return False

        return repo.delete(amenity)



class PlaceAmenity(Base):
    """PlaceAmenity representation"""

    __tablename__ = 'placeamenities'

    place_id = db.Column(db.String(120), nullable=False)
    amenity_id = db.Column(db.String(120), nullable=False)

    def __init__(self, place_id: str, amenity_id: str, **kw) -> None:
        """Initialize a PlaceAmenity instance"""
        super().__init__(**kw)
        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """String representation of PlaceAmenity"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Return dictionary representation of PlaceAmenity"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> Optional["PlaceAmenity"]:
        """Get a PlaceAmenity by place_id and amenity_id"""
        from src.persistence import repo

        all_place_amenities = PlaceAmenity.get_all()

        for place_amenity in all_place_amenities:
            if place_amenity.place_id == place_id and place_amenity.amenity_id == amenity_id:
                return place_amenity

        return None

    @staticmethod
    def get_all() -> list["PlaceAmenity"]:
        """Get all PlaceAmenity objects"""
        from src.persistence import repo

        return repo.get_all(PlaceAmenity.__tablename__)

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        from src.persistence import repo

        new_place_amenity = PlaceAmenity(**data)
        repo.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def update(entity_id: str, data: dict) -> Optional["PlaceAmenity"]:
        """Update an existing PlaceAmenity"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.get(entity_id)

        if not place_amenity:
            return None

        for key, value in data.items():
            setattr(place_amenity, key, value)

        repo.update(place_amenity)

        return place_amenity

    @staticmethod
    def delete(entity_id: str) -> bool:
        """Delete a PlaceAmenity by ID"""
        from src.persistence import repo

        place_amenity = PlaceAmenity.get(entity_id)

        if not place_amenity:
            return False

        return repo.delete(place_amenity)
