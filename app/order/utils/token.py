import os
from fastapi import HTTPException
from dotenv import load_dotenv
from jose import jwt

load_dotenv()
secret = os.environ["SECRET_KEY"]

def verifyToken(token: str):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload