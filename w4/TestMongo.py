from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
# dbweb.insert_one({"_id":2, "user_name":"Soumi"})
from collections import Counter
tokens = ["a"]
url = "dummy2.com"
index = {}
import re
pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')

for num in range(len(tokens)):
            
            print(index)
            #Remove None, punctuations and special characters tokens
            counter = Counter(tokens)
            if not tokens[num] or pattern.match(tokens[num]):
                continue
            if tokens[num] not in index:
                index[tokens[num]] = {url:counter[tokens[num]]}
                dbweb.insert_one({"key":tokens[num],"value":index[tokens[num]]})
            elif url not in index[tokens[num]]:
                index[tokens[num]].append({url:counter[tokens[num]]})
                dbweb.find_one_and_update({'key':tokens[num],"value":index[tokens[num]]})
                
            