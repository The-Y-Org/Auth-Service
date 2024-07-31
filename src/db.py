import motor.motor_asyncio

from settings import settings

url: str = f"mongodb://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_host}/"
client = motor.motor_asyncio.AsyncIOMotorClient(url)
common = client.get_database("common")
user_collection = common.get_collection("users")
