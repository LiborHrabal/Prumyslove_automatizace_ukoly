from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from pymongo import MongoClient
import datetime
import os

# Server configuration
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))

# MongoDB configuration
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "ukol03_mongodb")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "machine_data")

client = MongoClient(MONGO_HOST)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# --- JSON encoder for datetime objects ---
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj)

# --- HTTP request handler ---
class MyHandler(BaseHTTPRequestHandler):
    # GET request handler
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path.startswith("/machine_data"):
            try:
                # Filter parameters from query string 
                query_params = parse_qs(parsed.query)
                mongo_filter = {}

                for key, value in query_params.items():
                    # parse_qs vrací list, např. {"machine_id": ["M_01"]}
                    mongo_filter[key] = value[0]

                # načti data podle filtru
                docs = list(collection.find(mongo_filter, {"_id": 0}))

                # serializace
                response = json.dumps(docs, cls=CustomJSONEncoder).encode("utf-8")

                # odpověď
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)

            except Exception as e:
                self.send_error(500, f"Server error: {e}")

        else:
            self.send_error(404, "Not found")


def run():
    server = HTTPServer((HOST, PORT), MyHandler)
    print(f"Server běží na http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
