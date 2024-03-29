from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT

class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                print(credentials.credentials)
                raise HTTPException(status_code=403, detail='Invalid authentication scheme!')
            if not self.verify_jwt(credentials.credentials):
                print(credentials.credentials)
                raise HTTPException(status_code=403, detail='Invalid token or expired token!')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail='No authorization code or invalid authorization code!')

    def verify_jwt(self, jwttoken: str) -> bool:
        try:
            payload = decodeJWT(jwttoken)
            print('payload', payload)
            return bool(payload)
        except:
            return False
