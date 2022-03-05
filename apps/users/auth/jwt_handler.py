import time 
import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')

def token_response(token:str):
    return {"access token":token}

def singJWT(userID:str):
    payload = {
        "userID":userID,
        "expiry":time.time()+600
    }
    token = jwt.encode(payload,JWT_SECRET,JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token:str):
    try:
        decode_token = jwt.decode(token,JWT_SECRET,JWT_ALGORITHM)
        if decode_token.get('expiry') >= time.time():
            decode_token['expiry'] = time.time() + 900
            return decode_token
        return  None
    except Exception:
        return None