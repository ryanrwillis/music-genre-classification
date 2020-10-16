from pymongo import MongoClient

# Create a mongo connection
client = MongoClient("mongodb+srv://mongo:mongo2247@spotifysuperdata.tuo6e.gcp.mongodb.net/test")

# Have a look at all the databases in the client connection
print(client.list_database_names())

# Have a look at all the collection names in all the databases in client connection
for item in client.list_database_names():
    tempDB = client[item]
    print(f'Database: {item:<20}, Collections: {tempDB.list_collection_names()}')