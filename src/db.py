import motor.motor_asyncio

from settings import settings

url: str = f"mongodb://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_host}/"
client = motor.motor_asyncio.AsyncIOMotorClient(url)
users_db = client.get_database("users")
