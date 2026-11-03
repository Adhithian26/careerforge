import asyncio
import logging
import os
import socket
import sys
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.app.config import settings

logger = logging.getLogger("careerforge.mongodb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

def is_test_environment() -> bool:
    """Detects whether code is running under test runner or offline mock mode."""
    if os.environ.get("TESTING", "").lower() in ("1", "true"):
        return True
    if any("pytest" in arg.lower() for arg in sys.argv):
        return True
    if "pytest" in sys.modules:
        return True
    return False

def is_dns_reachable(timeout: float = 0.5) -> bool:
    """Fast non-blocking check to ensure external network/DNS is active before attempting SRV queries."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(("8.8.8.8", 53))
        sock.close()
        return True
    except Exception:
        return False

def get_mongodb_client() -> Optional[AsyncIOMotorClient]:
    """Returns the singleton Motor Async client, initializing it if necessary."""
    global _client
    if is_test_environment() or not settings.MONGODB_URL:
        return None

    if _client is None:
        if not is_dns_reachable(0.5):
            logger.info("External DNS unreachable; skipping MongoDB client initialization.")
            return None
        try:
            _client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                connect=False,
                serverSelectionTimeoutMS=1000,
                connectTimeoutMS=1000,
                socketTimeoutMS=1000
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
    """Verifies that the MongoDB Atlas cluster is reachable with a tight timeout."""
    if is_test_environment() or not settings.MONGODB_URL:
        return False

    client = get_mongodb_client()
    if not client:
        return False
    try:
        await asyncio.wait_for(client.admin.command("ping"), timeout=1.0)
        return True
    except Exception as e:
        logger.warning(f"MongoDB ping check failed: {e}")
        return False

def close_mongodb_connection():
    """Closes the MongoDB connection on shutdown."""
    global _client, _db
    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass
        _client = None
        _db = None
        logger.info("Closed MongoDB connection.")
