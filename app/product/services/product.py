from bson import ObjectId
from utils.database import Product
from serializers.product import product_serializer
from utils.validator import remove_none_values
from events.publisher.product import productCreatedPublisher, productUpdatedPublisher

async def createProduct(payload: dict):
    try:
        product = await Product.insert_one(payload)

        createdProduct = await Product.find_one({"_id": product.inserted_id})

        await productCreatedPublisher("product_created", createdProduct)

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


async def getProduct(id: str):
    try:
        product = await Product.find_one({"_id": ObjectId(id)})
        if not product:
            return None, "Product not found"

        return product_serializer(product), None
    except Exception as e:
        return None, str(e)


async def updateProduct(id: str, userId: str, payload: dict):
    try:
        productExists = await Product.find_one({"_id": ObjectId(id)},)
        if not productExists:
            return None, "Product not found"

        if str(productExists["createdBy"]) != userId:
            return None, "Not authorized to update this product"

        productUpdated = await Product.update_one({"_id": ObjectId(id)}, {"$set": remove_none_values(payload)})
        if not productUpdated:
            return None, "Error updating product"

        updatedProduct = await Product.find_one({"_id": ObjectId(id)})

        await productUpdatedPublisher("product_updated", updatedProduct)

        return productUpdated, None
    except Exception as e:
        return None, str(e)