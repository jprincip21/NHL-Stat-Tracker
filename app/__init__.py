__version__ = "1.0.0"

from utilities import get_games_by_date, get_image_default, get_image_light_dark # UTILITY IMPORTS
from .database.db_handler import initialize_database, update_display_mode, get_display_mode #DATABASE IMPORTS
from .gui import Application 

__all__ = [
    "Application",
    "get_games_by_date",
    "get_image_default",
    "get_image_light_dark",
    "initialize_database",
    "update_display_mode",
    "get_display_mode"
]