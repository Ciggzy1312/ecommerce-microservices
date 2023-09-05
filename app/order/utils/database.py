from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient('mongodb://order-db-srv:27017')

try:
    print("Connected to order database")
except Exception:
    print("Unable to connect to order database")

db = client.order
Order = db.order
Product = db.product