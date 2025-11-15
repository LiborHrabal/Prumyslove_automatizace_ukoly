import pandas as pd
import logging
from collections import deque
import time
from libs import mongo_basic   
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "ukol03_mongodb")   

chunk_size = 25
message_queue: deque[dict] = deque(maxlen=25) 

def read_date_from_csv_to_pd(path: str) -> pd.DataFrame:
    """Reads a CSV file into a pandas DataFrame."""
    dataset = pd.read_csv(path)
    return dataset


def collect_queue(data: pd.DataFrame):
    """Collects data into a fixed-size queue. """
    queue = []
    for row in data.itertuples(index=False):
        queue.append(row._asdict())
    return queue
            
""" 
        Template of a DB dat dictionary after reading from pd.DataFrame. One raw example:
        dict = {
            "plant_name": "Hala_A",
            "machine_id": "M_01",
            "timestamp": 2025-11-11 00:00:01,
            "temperature": 85.5,
            "power_usage": 12.3,
            "status": "operational",
            "machine_hours": 1500
        }
        
"""


def main():
    mongo_client, mongo_name = mongo_basic.connect_to_mongoDB(MONGO_HOST, DB_NAME)
    if mongo_client is None:
        logger.error("Failed to connect to MongoDB.")
        return  
    else: logger.info("Connected to MongoDB successfully.")

    collection_names = mongo_basic.get_collection_names(mongo_name)
    logger.info(f"Collections in the database: {collection_names}")

    data = read_date_from_csv_to_pd("data/machine_data.csv")
    
    for start in range(0, len(data), chunk_size):
        batch = data.iloc[start:start + chunk_size]
        queue = collect_queue(batch)
        if queue:
            mongo_basic.insert_multiple_data(mongo_name, "machine_data", list(queue))
            logger.info(f"Inserted batch of {len(queue)} records into MongoDB.")
        time.sleep(30)  # Simulate delay between batches 
        queue.clear()  # Clear the queue for the next batch
    

if __name__ == "__main__":
   main() 
   
   


    