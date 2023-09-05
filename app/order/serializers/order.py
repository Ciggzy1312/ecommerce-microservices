from bson import ObjectId

def order_serializer(order) -> dict:
    return {
        "_id": str(ObjectId(order["_id"])),
        "createdBy": str(ObjectId(order["createdBy"])),
        "status": order["status"],
        "expiresAt": order["expiresAt"].isoformat(),
        "product": {
            "_id": str(ObjectId(order["product"][0]["_id"])),
            "name": order["product"][0]["name"],
            "price": order["product"][0]["price"],
        },
    }