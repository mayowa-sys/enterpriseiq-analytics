import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not defined in environment variables")

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
db = client.enterpriseiq