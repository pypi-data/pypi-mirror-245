from typing import Optional

from ormspace.settings import SpaceSettings

class SpaceStarSettings(SpaceSettings):
    session_secret: Optional[str]
    csrf_secret: Optional[str]