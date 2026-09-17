# This file is used to import and expose the database models in the application.

from src.core.database.base import Base
from src.modules.auth.database.model import User

__all__ = ["Base", "User"]