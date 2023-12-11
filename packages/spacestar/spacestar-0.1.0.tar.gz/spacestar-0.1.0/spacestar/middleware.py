import os
from secrets import token_hex

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from spacestar.settings import SpaceStarSettings

settings = SpaceStarSettings()

session_middleware = Middleware(SessionMiddleware, secret_key=settings.session_secret)