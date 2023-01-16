from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
# dbweb.insert_one({"_id":2, "user_name":"Soumi"})
from collections import Counter
tokens = ["a"]
url = "dummy2.com"
index = {"key":"a","value":{"dummy1.com":"1"}}
import re
pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')

        #Pattern for removing most punctuations and special characters tokens
counter = Counter(tokens)
for token in tokens:
            #Remove None, punctuations and special characters tokens
    if not token or pattern.match(token):
        continue
    if token not in index.values()  :
        index[token] = {url:counter[token]}
        dbweb.insert_one({"key":token,"value":index[token]})
    elif url not in index["value"]:
        index["value"][url] = str(counter[token])
        dbweb.find_one_and_update({"key":token},{'$set':{"value":index["value"]}})
                
            