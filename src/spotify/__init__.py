"""Custom Spotify client"""

__version__ = "0.1.0"

from .client import Client as Client
from .user import User as User
from .track import Track as Track
from .harmony import Tonality as Tonality
from . import endpoints as endpoints
