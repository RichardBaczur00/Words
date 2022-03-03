from pydantic import BaseModel

from typing import Optional

class GameStartModel(BaseModel):
    game_id: str