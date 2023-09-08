import ast
from bson import ObjectId
from utils.validator import remove_none_values
from services.order import cancelOrder

from utils.database import Product

async def orderExpiredSubscriber(payload):
    try:
        payload = ast.literal_eval(payload)
        
        order, error = await cancelOrder(payload["_id"], ObjectId(payload["createdBy"]))
        if error:
            return None, error

        return "Successfully expired order", None
    except Exception as e:
        return None, str(e)