from bson import ObjectId

def user_serializer(user) -> dict:
    return {
        'id': str(ObjectId(user["_id"])),
        'username': user["username"],
        'email': user["email"]
    }