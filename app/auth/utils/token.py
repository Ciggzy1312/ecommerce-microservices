import os
from fastapi import HTTPException
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt

load_dotenv()
secret = os.environ["SECRET_KEY"]

async def generateToken(payload: dict):
    encode_payload = payload.copy()
    expire = datetime.utcnow() + timedelta(days=1)

    encode_payload['exp'] = expire
    encoded_jwt = jwt.encode(encode_payload, secret, algorithm="HS256")
    return encoded_jwt

def verifyToken(token: str):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload