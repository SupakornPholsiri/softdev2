from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']

dbweb.find_one_and_update({"key":"a"},{'$set':{"value":{"asdas":"sadasd"}}})
