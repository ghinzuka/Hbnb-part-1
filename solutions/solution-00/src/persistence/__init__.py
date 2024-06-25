""" This module is responsible for selecting the repository
to be used based on the environment variable REPOSITORY_ENV_VAR."""

import os

from src.persistence.repository import Repository
from src.persistence.db import DBRepository
from src.persistence.file import FileRepository
from src.persistence.pickled import PickleRepository
from src.persistence.memory import MemoryRepository
from utils.constants import REPOSITORY_ENV_VAR

repo: Repository

if os.getenv(key=REPOSITORY_ENV_VAR) == "db":
    repo = DBRepository()
elif os.getenv(REPOSITORY_ENV_VAR) == "file":
    repo = FileRepository()
elif os.getenv(REPOSITORY_ENV_VAR) == "pickle":
    repo = PickleRepository()
else:
    repo = MemoryRepository()

print(f"Using {repo.__class__.__name__} as repository")
