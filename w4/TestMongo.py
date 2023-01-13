from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
# dbweb.insert_one({"_id":2, "user_name":"Soumi"})
from collections import Counter
tokens = "M"
url = "dummy.com"
index = {}
import re
pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')

for token in tokens:
            #Remove None, punctuations and special characters tokens
            counter = Counter(token)
            if not token or pattern.match(token):
                continue
            if token not in index:
                index[token] = [counter[token],url]
                dbweb.insert_one({"key":token,"value":index[token]})
            elif url not in index[token]:
                index[token].append(url)
                dbweb.update_one({"key":token,"value":index[token]})