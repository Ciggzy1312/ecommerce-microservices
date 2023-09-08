import ast
from bson import ObjectId
from utils.validator import remove_none_values
from services.order import completeOrder

from utils.database import Product

async def paymentCompletedSubscriber(payload):
    try:
        payload = ast.literal_eval(payload)
        message, error = await completeOrder(payload["orderId"], ObjectId(payload["createdBy"]))
        if error:
            return None, error

        return message, None
    except Exception as e:
        return None, str(e)