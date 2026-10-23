import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.app.config import settings

logger = logging.getLogger("careerforge.mongodb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

def get_mongodb_client() -> Optional[AsyncIOMotorClient]:
    """Returns the singleton Motor Async client, initializing it if necessary."""
    global _client
    if _client is None and settings.MONGODB_URL:
        try:
            _client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000
            )
            logger.info("Initialized MongoDB Motor async client.")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB client: {e}")
            _client = None
    return _client

def get_mongodb_database() -> Optional[AsyncIOMotorDatabase]:
    """Returns the default MongoDB database instance."""
    global _db
    if _db is None:
        client = get_mongodb_client()
        if client:
            _db = client[settings.MONGODB_DB_NAME]
    return _db

async def ping_mongodb() -> bool:
    """Verifies that the MongoDB Atlas cluster is reachable."""
    client = get_mongodb_client()
    if not client:
        return False
    try:
        await client.admin.command("ping")
        return True
    except Exception as e:
        logger.warning(f"MongoDB ping check failed: {e}")
        return False

def close_mongodb_connection():
    """Closes the MongoDB connection on shutdown."""
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        logger.info("Closed MongoDB connection.")
