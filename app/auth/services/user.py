from bson import ObjectId
from utils.database import User
from utils import password, token
from serializers.user import user_serializer

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

async def loginUser(payload: dict):
    userExists = await User.find_one({"email": payload["email"]})
    if not userExists:
        return None, "User with this email does not exist"

    if not password.verifyPassword(payload["password"], userExists["password"]):
        return None, "Incorrect password"

    authToken = await token.generateToken(user_serializer(userExists))

    return authToken, None

async def getCurrentUser(payload: dict):
    user = await User.find_one({"_id": ObjectId(payload["id"])})
    if not user:
        return None, "User does not exist"

    return user_serializer(user), None