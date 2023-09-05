import ast
from bson import ObjectId
from utils.validator import remove_none_values

from utils.database import Product

async def orderCreatedSubscriber(payload):
    try:
        payload = ast.literal_eval(payload)
        product = await Product.update_one({"_id": ObjectId(payload["product"]["_id"])}, {"$set": {"orderId": payload["_id"]}})
        if not product:
            return None, "Product not found"

        return "Successfully reserved product in order service", None
    except Exception as e:
        return None, str(e)


async def orderCancelledSubscriber(payload):
    try:
        payload = ast.literal_eval(payload)
        product = await Product.update_one({"_id": ObjectId(payload["product"]["_id"])}, {"$set": {"orderId": None}})
        if not product:
            return None, "Product not found"

        return "Successfully unreserved product in order service", None
    except Exception as e:
        return None, str(e)