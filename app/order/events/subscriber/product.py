import ast
from bson import ObjectId
from utils.validator import remove_none_values
from serializers.product import product_serializer

from utils.database import Product

async def productCreatedSubscriber(payload):
    try:
        payload = product_serializer(ast.literal_eval(payload))
        product = await Product.insert_one(payload)
        print("Successfully created product in order service")

        return product, None
    except Exception as e:
        return None, str(e)


async def productUpdatedSubscriber(payload):
    try:
        payload = product_serializer(ast.literal_eval(payload))
        product = await Product.update_one({"_id": payload["_id"]}, {"$set": remove_none_values(payload)})
        print("Successfully updated product in order service")

        return product, None
    except Exception as e:
        return None, str(e)