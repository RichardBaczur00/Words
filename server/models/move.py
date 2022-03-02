from pydantic import BaseModel

from typing import Optional

class MoveModel(BaseModel):
    player_word: str