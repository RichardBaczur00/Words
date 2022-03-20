from pydantic import BaseModel

from typing import Optional


class StatSaveModel(BaseModel):
    user_id: str
    attempts: Optional[int]
    winner: bool