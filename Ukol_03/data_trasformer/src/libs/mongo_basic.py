""" Script for basic operations with mongoDB database for ukol03 """

import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timezone
import time

def connect_to_mongoDB(path: str, db_name: str) -> MongoClient:
    """ 
    Connect to MongoDB database 
    :param path: MongoDB connection string
    :param db_name: Name of the database to connect to
    
    :return: MongoDB database object    
    """
    try:
        client = MongoClient(path, serverSelectionTimeoutMS=5000)
        # Trigger a server selection to verify connection
        client.server_info()
        db = client[db_name]
        print(f"Connected to MongoDB database: {db_name}")
        return client, db
    except ConnectionFailure as e:
        logging.error(f"Could not connect to MongoDB: {e}")
        return None, None
    

def get_collection_names(db) -> list:
    """ 
    Get list of collection names in the database
    :param db: MongoDB database object
    :return: List of collection names
    """
    collection_names = db.list_collection_names()
    logging.info(f"Collections in the database: {collection_names}")
    return collection_names

def insert_simple_data(db, collection_name: str, data: dict):
    """ 
    Insert data into a MongoDB collection
    :param db: MongoDB database object
    :param collection_name: Name of the collection to insert data into
    :param data: Data to insert (as a dictionary)
    """
    collection = db[collection_name]
    result = collection.insert_one(data)
    logging.info(f"Inserted document with id: {result.inserted_id}")


def insert_multiple_data(db, collection_name: str, data_list: list[dict]):
    """ 
    Insert multiple data entries into a MongoDB collection
    :param db: MongoDB database object
    :param collection_name: Name of the collection to insert data into
    :param data_list: List of data dictionaries to insert
    """
    collection = db[collection_name]
    result = collection.insert_many(data_list)
    logging.info(f"Inserted {len(result.inserted_ids)} documents into collection '{collection_name}'")

def clear_collection(db, collection_name: str):
    """ 
    Clear all data from a MongoDB collection
    :param db: MongoDB database object
    :param collection_name: Name of the collection to clear
    """
    collection = db[collection_name]
    result = collection.delete_many({})
    logging.info(f"Cleared {result.deleted_count} documents from collection '{collection_name}'")

def read_data_from_collection(db, collection_name: str):
    """ 
    Read data from a MongoDB collection
    :param db: MongoDB database object
    :param collection_name: Name of the collection to read data from
    :return: List of documents in the collection
    """
    collection = db[collection_name]
    documents = list(collection.find())
    logging.info(f"Read {len(documents)} documents from collection '{collection_name}'")

    # Read documents with status "error" and log three previous documents
    read_errors = list(collection.find({"status": "error"}).sort("timestamp", - 1))
    count_errors = len(read_errors)
    logging.info(f"Found {count_errors} error documents.")
    for error in read_errors:
        logging.info(f"Error document: {error}")
        three_previous = collection.find(
            {"timestamp": {"$lt": error["timestamp"]}}
        ).sort("timestamp", -1).limit(3)
        for prev in three_previous:
            logging.info(f"Previous document before error: {prev}")

    # Read documents with temperature above 95°C and warn in log
    high_temp_docs = collection.find({"temperature": {"$gt": 95}})
    count_temperature_warnings = collection.count_documents({"temperature": {"$gt": 95}})
    logging.info(f"Found {count_temperature_warnings} high temperature documents.")
    for doc in high_temp_docs:
        logging.warning(f"High temperature document: {doc}")
    
    # Read documents with power usage over 14 kW and warn in log
    high_power_docs = collection.find({"power_usage": {"$gt": 14 }})
    count_power_warnings = collection.count_documents({"power_usage": {"$gt": 14}})
    logging.info(f"Found {count_power_warnings} high power usage documents.")
    for doc in high_power_docs:
        logging.warning(f"High power usage document: {doc}")


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    MONGO_HOST = "mongodb://localhost:27017/"
    DB_NAME = "ukol03_mongodb"
    COLLECTION_NAME = "machine_data"
    
    mongo_client, db = connect_to_mongoDB(MONGO_HOST, DB_NAME)
    if mongo_client is None:
        logger.error("Failed to connect to MongoDB.")
        return
    
    collection_names = get_collection_names(db)
    logger.info(f"Collections in the database: {collection_names}")

    # Clear collection before inserting new data  
    # clear_collection(db, COLLECTION_NAME)
    
    # Example data insertion
    sample_data = {
        "plant_name": "Hala_A",
        "machine_id": "M_01",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0),
        "temperature": 85.5,
        "power_usage": 12.3,
        "status": "operational",
        "machine_hours": 1500
    }
    insert_simple_data(db, COLLECTION_NAME, sample_data)
    
    time.sleep(3)
    # Example of inserting multiple data
    multiple_data = [
        {
            "plant_name": "Hala_A",
            "machine_id": "M_02",
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0),
            "temperature": 90.0,
            "power_usage": 13.5,
            "status": "operational",
            "machine_hours": 1200
        },
        {
            "plant_name": "Hala_A",
            "machine_id": "M_03",
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0),
            "temperature": 100.5,
            "power_usage": 15.0,
            "status": "error",
            "machine_hours": 800
        }
    ]
    insert_multiple_data(db, COLLECTION_NAME, multiple_data)
    
    # Read and log data from the collection
    read_data_from_collection(db, COLLECTION_NAME)
    
    mongo_client.close()
    
if __name__ == "__main__":
    main()















