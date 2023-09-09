import ast
from bson import ObjectId

from utils.database import Product

async def paymentCompletedSubscriber(payload):
    try:
        payload = ast.literal_eval(payload)
        product = await Product.update_one({"_id": ObjectId(payload["productId"])}, {"$set": {"orderId": None}})
        if not product:
            return None, "Product not found"

        return "Successfully unreserved product after payment complete", None
    except Exception as e:
        return None, str(e)