"""The first file that is run when running the twitoff package"""

from .app import create_app

APP = create_app()