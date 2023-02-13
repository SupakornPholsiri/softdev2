import re
import csv
import nltk
from nltk.stem import 	WordNetLemmatizer
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

    #Add or add onto keyword index using the tokens.
    def modify_index_with_tokens_no_mongo(self, tokens, url):
        #Pattern for removing most punctuations and special characters tokens
        pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')
        counter = Counter(tokens)
        for token in tokens:
            #Remove None, punctuations and special characters tokens
            if not token or pattern.match(token):
                continue
            if token not in self.index :
                self.index[token] = {url:counter[token]}
            elif url not in self.index[token]:
                self.index[token][url] = counter[token]
            elif url in self.index[token] and self.index[token][url] != counter[token]:
                self.index[token][url] = counter[token]
        return self.index

    #Save current index to csv file
    def save_to_file(self):
        with open('index2.csv', 'w', encoding="utf-8") as f:
            for key in self.index.keys():
                f.write(f'"{key}","{self.index[key]}"\n')
        f.close()

    def read_file(self):
        #Temporary used for output testing.
        with open('index2.csv', 'r', encoding="utf-8") as f:
            filecontent = csv.reader(f)
            for row in filecontent:
                print(row[0])
            self.index = {row[0]:eval(row[1]) for row in filecontent}
        f.close()

    def read_database(self):
        index = []
        for col in dbweb.find({},{"_id":0, "key":1, "value":1}):
            self.index[col["key"]] = col["value"]

    def search(self, query):
        try:
            return dbweb.find_one({"key":query})["value"]
        except:
            return "Keyword not found."
class ReferenceIndex :

    def __init__(self):
        self.ref_index = dict()
        self.ref_info = dict()

    def add_info_entry(self, url, base_domain, links):
        self.ref_info[url] = {"base_domain":base_domain, "links":links}

    def convert_info_to_index(self):
        for url in self.ref_info:
            info = self.ref_info[url]
            for link in info["links"]:
                if link.startswith(info["base_domain"]):
                    continue
                self.count_reference(link)

    #Add ref count
    def count_reference(self, link):
        if link not in self.ref_index:
            self.ref_index[link] = 1
        else:
            self.ref_index[link] += 1

    #Save current index to csv file
    def save_to_file(self):
        with open('ref_index.csv', 'w', encoding="utf-8") as f:
            for key in self.ref_index.keys():
                f.write(f'"{key}","{self.ref_index[key]}"\n')
        f.close()
    
    #ยังไม่ได้เชื่อม
    def lemmatization(self,tokens):
        wordnet_lemmatizer = WordNetLemmatizer()
        lemmatized = []
        for w in tokens:
            lemmatized.append(wordnet_lemmatizer.lemmatize(w))
        return lemmatized
    
