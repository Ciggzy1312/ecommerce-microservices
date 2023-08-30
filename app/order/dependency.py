from fastapi import Depends, Cookie
from datetime import timedelta
from jose import jwt

from utils.token import verifyToken


def get_current_user(token: str = Cookie(None)):
    payload = verifyToken(token)
    return payload