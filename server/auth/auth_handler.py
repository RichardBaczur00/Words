import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')

def token_response(token: str) -> Dict[str, str]:
    return {
        'access_token': token
    }


def signJWT(user_id: str, game_id: str) -> Dict[str, str]:
    payload = {
        'user_id': str(user_id),
        'game_id': str(game_id),
        'role': 'player',
        'expires': time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    return decoded_token if decoded_token['expires'] >= time.time() else None