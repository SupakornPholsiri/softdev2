import re
import csv
from pymongo import MongoClient
from collections import Counter

class Database:
    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.SearchEngine = self.client['TestSearchEngine']
        self.raw_data_storage = self.SearchEngine["RawData"]
        self.dbweb = self.SearchEngine['WebDB']

class RawInfoIndex:
    def __init__(self):
        self.index = {}
        self.url_to_be_updated = set()

    #Add or add onto keyword index using the tokens.
    def modify_index(self, url:str, raw_text:str, links:set, hash:str):
        if url not in self.index:
            self.index[url] = {"text":raw_text, "links":links, "hash":hash}
            self.url_to_be_updated.add(url)
        elif self.index[url]["hash"] != hash:
            self.index[url] = {"text":raw_text, "links":links, "hash":hash}
            self.url_to_be_updated.add(url)
        """else :
            self.index[url] = {"text":raw_text, "links":links, "hash":hash}"""
        return self.index

    def save_to_database(self, database):
        raw_data_collection = database["RawData"]
        for url in self.index:
            if url in self.url_to_be_updated:
                if raw_data_collection.find_one({"key":url}):
                    raw_data_collection.find_one_and_update({"key":url},{"$set":{  "text":self.index[url]["text"],
                                                                        "links":{str(i):self.index[url]["links"][i] for i in range(len(self.index[url]["links"]))},
                                                                        "hash":self.index[url]["hash"]}})
                else:
                    raw_data_collection.insert_one({"key":url,
                                                    "text":self.index[url]["text"],
                                                    "links":{str(i):self.index[url]["links"][i] for i in range(len(self.index[url]["links"]))},
                                                    "hash":self.index[url]["hash"]})
                self.url_to_be_updated.remove(url)

    def read_from_database(self, database):
        raw_data_collection = database["RawData"]
        self.index = {}
        for col in raw_data_collection.find({},{"_id":0, "key":1, "text":1, "links":1, "hash":1}):
            links = [col["links"][i] for i in col["links"]]
            self.index[col["key"]] = {"text":col["text"], "links":links, "hash":col["hash"]}

    
    """def save_to_file(self):
        with open('Raw_info.csv', 'w', encoding="utf-8") as f:
            for key in self.index.keys():
                f.write(f'"{key}","{self.index[key]["text"]}","{self.index[key]["links"]}","{self.index[key]["hash"]}"\n')
        f.close()

    def read_file(self):
        #Temporary used for output testing.
        with open('Raw_info.csv', 'r', encoding="utf-8") as f:
            filecontent = csv.reader(f, quotechar='"')
            self.index = {row[0]:{"text":row[1], "links":eval(row[2]), "hash":row[3]} for row in filecontent}
        f.close()"""

class InvertedIndex:
    #Class for indexes. Methods related to index are stored here.

    def __init__(self):
        self.index = {}
        self.keywords_to_be_updated = set()

    """ #Add or add onto keyword index using the tokens.
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
        return self.index"""

    #Add or add onto keyword index using the tokens.
    def modify_index_with_tokens(self, tokens, url):
        counter = Counter(tokens)
        for token in tokens:
            if token not in self.index :
                self.index[token] = {url:counter[token]}
            elif url not in self.index[token]:
                self.index[token][url] = counter[token]
            elif self.index[token][url] != counter[token]:
                self.index[token][url] = counter[token]
            else:
                continue
            self.keywords_to_be_updated.add(token)
        return self.index

    """#Save current index to csv file
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
"""
    def save_to_database(self, database):
        inverted_collection = database["WebDB"]
        for keyword in self.index:
            if keyword in self.keywords_to_be_updated:
                if inverted_collection.find_one({"key":keyword}):
                    inverted_collection.find_one_and_update({"key":keyword},{"$set":{"value":self.index[keyword]}})
                else:
                    inverted_collection.insert_one({"key":keyword, "value":self.index[keyword]})
                self.keywords_to_be_updated.remove(keyword)

    def read_from_database(self, database):
        inverted_collection = database["WebDB"]
        self.index = {}
        for col in inverted_collection.find({},{"_id":0, "key":1, "value":1}):
            self.index[col["key"]] = col["value"]
class ForwardIndex :

    def __init__(self):
        self.index = {}
        self.urls_to_be_updated = set()
        self.locations = []

    def get_location_info(self, url, tokens):
        if url not in self.index:
            self.index[url] = {}
        self.index[url]["Location"] = {}
        for token in tokens:
            if token in self.locations:
                self.index[url]["Location"][f"{len(self.index[url]['Location'])-1}"] = token

    def modify_ref_count(self, url:str, links:list[str], base_domains:list[str]):
        for link in links:
            print(link)
            domain = link.split("/")[2]
            if domain not in base_domains or domain == url.split("/")[2]:
                continue
            self.count_reference(url)
    
    #Add ref count
    def count_reference(self, url:str):
        if url not in self.index:
            self.index[url]["Refcount"] = 1
        else:
            self.index[url]["RefCount"] += 1

    def modify_index(self, url:str, links:list[str], tokens:list[str], base_domains:list[str]):
        location = self.get_location_info(url, tokens)
        self.modify_ref_count(url, links, base_domains)
        if url not in self.index:
            self.index[url]["Location"] = location
        elif self.index[url]["Location"] != location:
            self.index[url]["Location"] = location
        else:
            return self.index
        return self.index

    def save_to_database(self, database):
        forward_database = database["FWIndex"]
        for url in self.urls_to_be_updated:
            pass

    def read_from_database(self, database):
        pass