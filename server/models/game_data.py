from pydantic import BaseModel

from typing import Optional


class GameDataModel(BaseModel):
    game_id: str
    lives: int
    score: int