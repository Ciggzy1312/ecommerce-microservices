from utils.database import User
from utils import password

async def registerUser(payload: dict):
    try:
        userExists = await User.find_one({"email": payload["email"]})
        if userExists:
            return None, "User with this email already exists"

        payload["password"] = password.hashPassword(payload["password"])

        userInserted = await User.insert_one(payload)
        return userInserted, None
    except Exception as e:
        print(e)
        return None, str(e)