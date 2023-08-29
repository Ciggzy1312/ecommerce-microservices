from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient('mongodb://product-db-srv:27017')

try:
    print("Connected to product database")
except Exception:
    print("Unable to connect to product database")

db = client.product
Product = db.product