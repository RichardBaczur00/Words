from pydantic import BaseModel

from typing import Optional

class UserModel(BaseModel):
    user_id: str