"""
City related functionality
"""

from src.models.base import Base
from src.models.country import Country
from src.persistence import repo
from src import db


class City(Base):
    """City representation"""

    __tablename__ = 'cities'

    name = db.Column(db.String(120), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)

    def __init__(self, name: str, country_code: str, **kwargs) -> None:
        """City initializer"""
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """String representation of City"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        country = Country.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        new_city = City(**data)

        repo.save(new_city)

        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city

    @classmethod
    def get(cls, city_id: str) -> "City":
        """Get a city by ID"""
        return repo.get(cls.__name__.lower(), city_id)

    @classmethod
    def get_all(cls) -> list["City"]:
        """Get all cities"""
        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, city_id: str) -> bool:
        """Delete a city by ID"""
        city = cls.get(city_id)

        if not city:
            return False

        return repo.delete(city)
