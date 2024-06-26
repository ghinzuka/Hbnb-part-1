from src.models.base import Base
from src import db
from src.persistence import repo
from src.models.city import City


class Country():
    """
    Country representation
    """

    __tablename__ = 'countries'

    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(2), nullable=False, unique=True)

    cities = db.relationship("City", backref="country", lazy="dynamic")

    def __init__(self, name: str, code: str, **kwargs) -> None:
        """Country initializer"""
        super().__init__(**kwargs)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """String representation of Country"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        return repo.get_all("countries")

    @staticmethod
    def get_by_code(code: str) -> "Country | None":
        """Get a country by its code"""
        return repo.get("countries", code)

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        new_country = Country(name=name, code=code)
        repo.save(new_country)
        return new_country
