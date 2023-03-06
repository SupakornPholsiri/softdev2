import re
import csv
from pymongo import MongoClient
from collections import Counter

class Database:
    def __init__(self, client='localhost:27017', SearchEngine='SearchEngine', raw_data_storage="RawData", dbweb='WebDB', fw_index="FWIndex"):
        self.client = MongoClient(client)
        self.SearchEngine = self.client[SearchEngine]
        self.raw_data_storage = self.SearchEngine[raw_data_storage]
        self.dbweb = self.SearchEngine[dbweb]
        self.fw_index = self.SearchEngine[fw_index]

class RawInfoIndex:
    def __init__(self):
        """Initialize the RawInfoIndex and its variables"""
        self.index = {}
        self.url_to_be_updated = set()
        self.url_to_be_deleted = []
        self.in_queue_deleted = 0

    def get_urls(self):
        """Get a list of URLs in the index"""
        return [url for url in self.index]

    def modify_index(self, url:str, raw_text:str, links:set, hash:str):
        """Insert new url index or edit the existing one"""
        long_spaced_text = re.sub(r"[\n\t]", " ", raw_text)
        text = re.sub(r" +", " ", long_spaced_text)

        if url not in self.index:
            self.index[url] = {"text":text, "links":links, "hash":hash}
            self.url_to_be_updated.add(url)
        elif self.index[url]["hash"] != hash:
            self.index[url] = {"text":text, "links":links, "hash":hash}
            self.url_to_be_updated.add(url)
        return self.index

    def remove_urls(self, urls:list[str]):
        """Remove existing url indices"""
        for url in urls:
            if url in self.index:
                del self.index[url]
                self.url_to_be_deleted.append(url)

    def save_to_database(self, database:Database):
        """Save the raw data to Mongo database"""
        raw_data_collection = database.raw_data_storage
        for url in self.index:
            if url in self.url_to_be_updated:
                if not raw_data_collection.find_one_and_update({"key":url},
                        {"$set":{"text":self.index[url]["text"],
                        "links":{str(i):self.index[url]["links"][i] for i in range(len(self.index[url]["links"]))},
                        "hash":self.index[url]["hash"]}}):

                    raw_data_collection.insert_one({"key":url,
                                                    "text":self.index[url]["text"],
                                                    "links":{str(i):self.index[url]["links"][i] for i in range(len(self.index[url]["links"]))},
                                                    "hash":self.index[url]["hash"]})
                self.url_to_be_updated.remove(url)

        for url in self.url_to_be_deleted:
            raw_data_collection.delete_one({"key":url})
            self.in_queue_deleted += 1

    def read_from_database(self, database:Database):
        """Read raw data from the database and modify the index accordingly"""
        raw_data_collection = database.raw_data_storage
        self.index = {}
        for col in raw_data_collection.find({},{"_id":0, "key":1, "text":1, "links":1, "hash":1}):
            links = [col["links"][i] for i in col["links"]]
            self.index[col["key"]] = {"text":col["text"], "links":links, "hash":col["hash"]}

    def get_ref_count(self, url:str):
        ref_count = 0
        if url in self.index:
            for key in self.index:
                if url in self.index[key]["links"] and key.split("/")[2] != url.split("/")[2]:
                    ref_count += 1
        return ref_count
    
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
        self.keywords_to_be_removed = []
        self.in_queue_deleted = 0

    #Add or add onto keyword index using the tokens.
    def modify_index_with_tokens(self, tokens:list[str], removed_keywords:set[str], url:str):
        """Edit keyword index using the tokens"""
        self.remove_url_from_keywords(url, removed_keywords)
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

    def remove_url_from_keywords(self, url:str, removed_keywords:set|str="*"):
        """Remove URL from the keyword that the website no longer have\n
        and remove the keyword if there is no more website that have the keyword."""
        if removed_keywords == "*":
            removed_keywords = self.index.keys()

        for keyword in removed_keywords:

            if url in self.index[keyword]:
                del self.index[keyword][url]
                self.keywords_to_be_updated.add(keyword)

                if len(self.index[keyword]) == 0:
                    del self.index[keyword]
                    self.keywords_to_be_updated.remove(keyword)
                    self.keywords_to_be_removed.append(keyword)

    """def remove_missing_urls(self, urls:list[str]):
        Remove URLs from the index
        for keyword in self.index:
            for u in self.index[keyword]:
                if u not in urls:
                    del self.index[keyword][u]"""

    def save_to_database(self, database:Database):
        inverted_collection = database.dbweb
        for keyword in self.index:
            if keyword in self.keywords_to_be_updated:
                if not inverted_collection.find_one_and_update({"key":keyword},{"$set":{"value":self.index[keyword]}}):
                    inverted_collection.insert_one({"key":keyword, "value":self.index[keyword]})
                self.keywords_to_be_updated.remove(keyword)
            if keyword in self.keywords_to_be_removed:
                inverted_collection.delete_one({"key":keyword})
                self.keywords_to_be_removed.remove(keyword)

    def read_from_database(self, database:Database):
        inverted_collection = database.dbweb
        self.index = {}
        for col in inverted_collection.find({},{"_id":0, "key":1, "value":1}):
            self.index[col["key"]] = col["value"]

class ForwardIndex :

    def __init__(self):
        self.index = {}
        self.urls_to_be_updated = set()
        self.missing_keywords_dict = dict()
        self.urls_to_be_removed = []
        self.in_queue_removed = 0
        self.locations = []

    def find_missing_keywords_in_url(self, url:str, new_keywords:dict):
        missing_keywords = set()
        for keyword in self.index[url]["Keywords"]:
            if keyword not in new_keywords:
                missing_keywords.add(keyword)
            self.missing_keywords_dict[url] = missing_keywords
        return missing_keywords

    def get_location_info(self, url, tokens):
        if url not in self.index:
            self.index[url] = {}
        self.index[url]["Location"] = {}
        for token in tokens:
            if token in self.locations:
                self.index[url]["Location"][f"{len(self.index[url]['Location'])}"] = token

    def modify_ref_count(self, url:str, links:list[str], base_domains:list[str]):
        for link in links:
            domain = link.split("/")[2]
            if domain not in base_domains or domain == url.split("/")[2]:
                continue
            print("Should be something here")
            self.count_reference(link)
    
    #Add ref count
    def count_reference(self, url:str):
        if url not in self.index:
            self.index[url] = {"Location":None,"RefCount":1}
        elif "RefCount" not in self.index[url]:
            self.index[url]["RefCount"] = 1
        else:
            self.index[url]["RefCount"] += 1

    def modify_index(self, url:str, links:list[str], tokens, base_domains:list[str]):
        counter = Counter(tokens)
        location = self.get_location_info(url, tokens)
        self.modify_ref_count(url, links, base_domains)
        if url not in self.index:
            self.index[url]["Location"] = location
            self.index[url]["Keywords"] = counter
        elif self.index[url]["Location"] != location:
            self.index[url]["Location"] = location
            self.index[url]["Keywords"] = counter
        else:
            return self.index
        return self.index

    def clean(self, raw_index_urls):
        for key in self.index:
            if key not in raw_index_urls:
                del self.index[key]
                self.urls_to_be_removed.append(key)
            elif "RefCount" not in self.index[key]:
                self.index[key]["RefCount"] = 0

    def save_to_database(self, database:Database):
        for url in self.index:
            if url in self.urls_to_be_updated:
                if not database.fw_index.find_one_and_update({"key":url}, {"$set":{"value":self.index[url]}}):
                    database.fw_index.insert_one({"key":url,"value":{"Keywords":self.index[url]["Keywords"],
                                                                     "Location":self.index[url]["Location"],
                                                                     "RefCount":self.index[url]["RefCount"]}})
                self.urls_to_be_updated.remove(url)

        for url in self.urls_to_be_removed:
            database.fw_index.delete_one({"key":url})
            self.in_queue_removed += 1

    def read_from_database(self, database:Database):
        self.index = {}
        for col in database.fw_index.find({},{"_id":0, "key":1, "value":1}):
            self.index[col["keys"]] = col["value"]

class Index:
    #Class for indexes. Methods related to index are stored here.

    def __init__(self):
        self.ivi_index = {}
        self.fw_index = {}

        self.urls_in_queue = []
        self.urls_queue_front = 0

        self.urls_to_be_updated = set()
        self.urls_to_be_removed = []
        self.urls_removed_from_database = 0

        self.locations = []

        self.keywords_to_be_updated = set()
        self.keywords_to_be_removed = []
        self.keywords_removed_from_database = 0

    def remove_urls(self, urls_to_be_removed:list[str]):
        for url in urls_to_be_removed:
            if url in self.fw_index:
                self.modify_ivi_index([], "*", url)
                del self.fw_index[url]

    def modify_index(self,url:str, tokens):
        """Add or edit document of both the forward index and inverted index"""
        self.modify_ivi_index(tokens, self.find_missing_keywords_in_url(url, tokens), url)
        self.modify_fw_index(url,tokens)

    def modify_fw_index(self, url:str, tokens:dict):
        """Add or edit forward index"""
        location = self.get_location_info(tokens)
        if url not in self.fw_index:
            self.fw_index[url] = {"Keywords":tokens, "Location":location}
        elif self.fw_index[url] != {"Keywords":tokens, "Location":location}:
            self.fw_index[url]["Location"] = location
            self.fw_index[url]["Keywords"] = tokens
        else:
            return self.fw_index
        self.urls_to_be_updated.add(url)
        return self.fw_index

    #Add or add onto keyword index using the tokens.
    def modify_ivi_index(self, tokens:dict, removed_keywords:set[str]|str, url:str):
        """Edit keyword index using the tokens"""
        self.remove_url_from_keywords(url, removed_keywords)
        for token in tokens:
            if token not in self.ivi_index :
                self.ivi_index[token] = {url:tokens[token]}
            elif url not in self.ivi_index[token]:
                self.ivi_index[token][url] = tokens[token]
            elif self.ivi_index[token][url] != tokens[token]:
                self.ivi_index[token][url] = tokens[token]
            else:
                continue
            self.keywords_to_be_updated.add(token)
        return self.ivi_index

    def remove_url_from_keywords(self, url:str, removed_keywords:set|str="*"):
        """Remove URL from the keyword that the website no longer have\n
        and remove the keyword if there is no more website that have the keyword."""
        if removed_keywords == "*":
            removed_keywords = set(self.ivi_index.keys())

        for keyword in removed_keywords:

            if url in self.ivi_index[keyword]:
                del self.ivi_index[keyword][url]
                self.keywords_to_be_updated.add(keyword)

                if len(self.ivi_index[keyword]) == 0:
                    del self.ivi_index[keyword]
                    self.keywords_to_be_updated.remove(keyword)
                    self.keywords_to_be_removed.append(keyword)

    def find_missing_keywords_in_url(self, url:str, new_keywords:dict):
        missing_keywords = set()
        for keyword in self.fw_index[url]["Keywords"]:
            if keyword not in new_keywords:
                missing_keywords.add(keyword)
        return missing_keywords

    def get_location_info(self, tokens:dict):
        location = {}
        for token in tokens:
            if token in self.locations:
                location[token] = tokens[token]
        return location

    def save_ivi_index_to_database(self, database:Database):
        inverted_collection = database.dbweb
        for keyword in self.ivi_index:
            if keyword in self.keywords_to_be_updated:
                if not inverted_collection.find_one_and_update({"key":keyword},{"$set":{"value":self.ivi_index[keyword]}}):
                    inverted_collection.insert_one({"key":keyword, "value":self.ivi_index[keyword]})
                self.keywords_to_be_updated.remove(keyword)
        for keyword in self.keywords_to_be_removed:
            inverted_collection.delete_one({"key":keyword})
            self.keywords_removed_from_database += 1

    def read_ivi_index_from_database(self, database:Database):
        inverted_collection = database.dbweb
        self.ivi_index = {}
        for col in inverted_collection.find({},{"_id":0, "key":1, "value":1}):
            self.ivi_index[col["key"]] = col["value"]

    def save_fw_index_to_database(self, database:Database):
        for url in self.fw_index:
            if url in self.urls_to_be_updated:
                if not database.fw_index.find_one_and_update({"key":url}, {"$set":{"value":self.fw_index[url]}}):
                    database.fw_index.insert_one({"key":url,"value":{"Keywords":self.fw_index[url]["Keywords"],
                                                                     "Location":self.fw_index[url]["Location"]}})
                self.urls_to_be_updated.remove(url)

        for url in self.urls_to_be_removed:
            database.fw_index.delete_one({"key":url})
            self.urls_removed_from_database += 1
            

    def read_fw_index_from_database(self, database:Database):
        self.fw_index = {}
        for col in database.fw_index.find({},{"_id":0, "key":1, "value":1}):
            self.fw_index[col["key"]] = col["value"]