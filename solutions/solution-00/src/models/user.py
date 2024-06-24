"""
User related functionality
"""

from src.models.base import Base
from src import db
from typing import Optional


class User(Base):
    """User representation"""

    email = db.Column(db.String(120),unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.column(db.Boolean, default=False)

    def __init__(self, email: str, first_name: str, last_name: str, password: str, is_admin: bool = False, **kw):
        """Dummy init"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_amdin = is_admin
        self.password = password

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        from src.persistence import repo

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        repo.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> Optional["User"]:
        """Update an existing user"""
        from src.persistence import repo

        user: Optional[User] = User.get(user_id)

        if not user:
            return None

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        repo.update(user)

        return user

    @classmethod
    def get(cls, user_id: str) -> Optional["User"]:
        """Get a user by ID"""
        from src.persistence import repo

        return repo.get(cls.__name__.lower(), user_id)

    @classmethod
    def get_all(cls) -> list["User"]:
        """Get all users"""
        from src.persistence import repo

        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, user_id: str) -> bool:
        """Delete a user by ID"""
        from src.persistence import repo

        user = cls.get(user_id)
        if not user:
            return False

        return repo.delete(user)