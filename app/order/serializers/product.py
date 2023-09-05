from bson import ObjectId

def product_serializer(product) -> dict:
    return {
        "_id": ObjectId(product["_id"]),
        "name": product["name"],
        "price": product["price"],
    }