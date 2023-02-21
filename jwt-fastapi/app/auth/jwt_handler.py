#  Signing,encoding,decoding and returning JWTs

import time
import jwt


JWT_SECRET = 'secretkey123'
JWT_ALGORITHM = 'HS256'


# func returns generated tokens
def token_response(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token:str):
    try:
        decode_token = jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {
            "error":"invalid"
        }



