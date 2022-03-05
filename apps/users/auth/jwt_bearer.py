from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from .jwt_handler import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self,auto_error:bool=True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
    
    async def __call__(self,request:Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,detail="Invalida authorization schema")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail='Invalid token or expired')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,detail='Invalid authorization code')
            
    def verify_jwt(self,jwttoken:str):
        try:
            payload = decodeJWT(jwttoken)
        except:
            payload = None
        return bool(payload)