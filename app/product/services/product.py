from utils.database import Product
from serializers.product import product_serializer

async def createProduct(payload: dict):
    try:
        product = await Product.insert_one(payload)
        return product, None
    except Exception as e:
        return None, str(e)


async def getProducts():
    try:
        productsList = []
        async for product in Product.find():
            productsList.append(product_serializer(product))
        return productsList, None
    except Exception as e:
        return None, str(e)