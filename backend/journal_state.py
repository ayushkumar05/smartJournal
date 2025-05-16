from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = "shared_journal"
COLLECTION_NAME = "entries"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

JOURNAL_ID = "main"

async def get_journal():
    doc = await collection.find_one({"_id": JOURNAL_ID})
    if doc:
        return {"text": doc["text"]}
    else:
        return {"text": ""}

async def update_journal(text: str):
    await collection.update_one(
        {"_id": JOURNAL_ID},
        {"$set": {"text": text}},
        upsert=True
    )
