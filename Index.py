import re
import csv
from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
from collections import Counter

class Index:
    #Class for indexes. Methods related to index are stored here.

    def __init__(self):
        self.index = {}

    #Add or add onto keyword index using the tokens.
    def modify_index_with_tokens(self, tokens, url):
        #Pattern for removing most punctuations and special characters tokens
        pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')
        counter = Counter(tokens)
        for token in tokens:
            #Remove None, punctuations and special characters tokens
            if not token or pattern.match(token):
                continue
            if token not in self.index :
                self.index[token] = {url:counter[token]}
                dbweb.insert_one({"key":token,"value":self.index[token]})
            elif url not in self.index[token]:
                self.index[token][url] = counter[token]
                dbweb.find_one_and_update({"key":token},{'$set':{"value":self.index[token]}})
            elif url in self.index[token] and self.index[token][url] != counter[token]:
                self.index[token][url] = counter[token]
                dbweb.find_one_and_update({"key":token},{'$set':{"value":self.index[token]}})
        return self.index

    #Save current index to csv file
    def save_to_file(self):
        with open('index.csv', 'w', encoding="utf-8") as f:
            for key in self.index.keys():
                f.write(f'"{key}","{self.index[key]}"\n')
        f.close()

    def read_file(self):
        #Temporary used for output testing.
        with open('index.csv', 'r', encoding="utf-8") as f:
            filecontent = csv.reader(f)
            self.index = {row[0]:eval(row[1]) for row in filecontent}
        f.close()