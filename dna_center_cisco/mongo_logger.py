# dna_center_cisco/mongo_logger.py

from datetime import datetime

from django.conf import settings
from pymongo import MongoClient


def log_interaction(action, device_ip=None, success=True, error=None):
    """
    Insert a single interaction log document into MongoDB.

    This function should never break the main application flow:
    any MongoDB connection or insert error is caught and only printed.
    """
    try:
        client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
        db = client[settings.MONGODB_DB_NAME]
        collection = db[settings.MONGODB_COLLECTION]

        doc = {
            "timestamp": datetime.utcnow(),
            "action": action,
            "device_ip": device_ip,
            "success": bool(success),
            "error": str(error) if error else None,
        }
        collection.insert_one(doc)
    except Exception as e:
        # If logging to MongoDB fails, just print the error and do not crash the app
        print(f"[MongoLogger] failed to log interaction: {e}")