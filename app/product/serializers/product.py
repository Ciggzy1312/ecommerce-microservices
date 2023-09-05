from bson import ObjectId

def product_serializer(product) -> dict:
    return {
        'id': str(ObjectId(product["_id"])),
        'name': product["name"],
        'description': product["description"],
        'price': product["price"],
        'orderId': product["orderId"] if product.get("orderId") else None,
        'createdBy': str(ObjectId(product["createdBy"])),
    }