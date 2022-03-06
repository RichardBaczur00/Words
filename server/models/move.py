from pydantic import BaseModel

from typing import Optional

class MoveModel(BaseModel):
    user_id: str
    game_id: str
    player_word: str