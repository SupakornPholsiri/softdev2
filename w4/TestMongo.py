from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
dbweb.insert_one({"_id":2, "user_name":"Soumi"})