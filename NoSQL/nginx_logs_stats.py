#!/usr/bin/env python3

from pymongo import MongoClient

# Connection URL
url = "mongodb://localhost:27017/"

# Connect to MongoDB
client = MongoClient(url)

# Access the logs database
db = client["logs"]

# Access the nginx collection
collection = db["nginx"]

# Get total number of logs
total_logs = collection.count_documents({})

# Print total number of logs
print(f"{total_logs} logs where {total_logs} is the number of documents in this collection")

# Get count of logs for each method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = collection.count_documents({"method": method})
    print(f"\t{count} {method}")

# Get count of logs with method=GET and path=/status
status_count = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{status_count} logs where method=GET and path=/status")

# Close connection
client.close()
