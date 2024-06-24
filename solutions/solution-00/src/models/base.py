""" Abstract base class for all models """

from datetime import datetime
from typing import Any, Optional, Type, TypeVar
import uuid
from abc import ABC, abstractmethod
from src import db

T = TypeVar('T', bound='Base')

class Base(ABC):
    """
    Base Interface for all models
    """
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """

        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    continue
                setattr(self, key, value)

        self.id = str(id or uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def get(cls: Type[T], id: str) -> Optional[T]:
        """
        Get a specific object of a class by its id
        """
        from src.persistence import repo

        return repo.get(cls.__name__.lower(), id)

    @classmethod
    def get_all(cls: Type[T]) -> list[T]:
        """
        Get all objects of a class
        """
        from src.persistence import repo

        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls: Type[T], id: str) -> bool:
        """
        Delete a specific object of a class by its id
        """
        from src.persistence import repo

        obj = cls.get(id)

        if not obj:
            return False

        return repo.delete(obj)

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Optional[Any]:
        """Updates an object of the class"""
