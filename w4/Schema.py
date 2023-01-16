from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
find = dbweb.find_one({"key":"a"})

token = {"key":"a","value":{"url":"5"}}
print(token.values())
if "a" in token.values():
    print("F")