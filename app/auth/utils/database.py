from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient('mongodb://auth-db-srv:27017')

try:
    print("Connected to MongoDB")
except Exception:
    print("Unable to connect to MongoDB")

db = client.auth
User = db.user