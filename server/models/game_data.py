from pydantic import BaseModel
from pydantic.typing import Dict

from typing import Any, Optional


class GameDataModel(BaseModel):
    game: Dict[str, Any]
    game_id: str
    game_token: str    

