from pydantic import BaseModel

from typing import Optional


class JoinGameModel(BaseModel):
    user_id: str
    game_id: str