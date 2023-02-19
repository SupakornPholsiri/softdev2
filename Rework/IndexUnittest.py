import unittest
from unittest.mock import patch, MagicMock, call
import mongomock
from IndexV2 import RawInfoIndex
from pymongo import MongoClient
from IndexV2 import InvertedIndex
class RawInfoTest(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()
        self.rawInfo = RawInfoIndex()
        self.testDB = MongoClient('localhost:27017')["TestSearchEngine"]

    def tearDown(self):
        self.testDB.drop_collection("RawData")
    
    def test_init(self):
        assert self.rawInfo.index == {}
        assert self.rawInfo.url_to_be_updated == set()
        assert self.rawInfo.url_to_be_deleted == []
        assert self.rawInfo.in_queue_deleted == 0

    def test_modify_index_new(self):
        self.rawInfo.index = {"https://www.example.com":
        {"text":"A",
        "links":[],
        "hash":"131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d"}}

        self.rawInfo.modify_index("https://www.test.com",
        "B",
        ["https://www.dummy.com"], 
        "8ce2c05fc4d1d4beb81ab0e25cb606b26e5ffcb090b7fe08187760ff74c1db63")

        self.assertEqual(self.rawInfo.index, {"https://www.example.com":
        {"text":"A",
        "links":[],
        "hash":"131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d"},
        "https://www.test.com":
        {"text":"B",
        "links":["https://www.dummy.com"],
        "hash":"8ce2c05fc4d1d4beb81ab0e25cb606b26e5ffcb090b7fe08187760ff74c1db63"}})

        self.assertEqual(self.rawInfo.url_to_be_updated, {"https://www.test.com"})

    def test_modify_index_update(self):
        self.rawInfo.index = {"https://www.example.com":
        {"text":"A",
        "links":[], 
        "hash":"131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d"}}

        self.rawInfo.modify_index("https://www.example.com", 
        "B", 
        ["https://www.dummy.com"], 
        "8ce2c05fc4d1d4beb81ab0e25cb606b26e5ffcb090b7fe08187760ff74c1db63")

        self.assertEqual(self.rawInfo.index, {"https://www.example.com":
        {"text":"B", 
        "links":["https://www.dummy.com"], 
        "hash":"8ce2c05fc4d1d4beb81ab0e25cb606b26e5ffcb090b7fe08187760ff74c1db63"}})

        self.assertEqual(self.rawInfo.url_to_be_updated, {"https://www.example.com"})

    def test_modify_index_duplicate(self):
        self.rawInfo.index = {"https://www.example.com":
        {"text":"A", 
        "links":[], 
        "hash":"131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d"}}

        self.rawInfo.modify_index("https://www.example.com", "A", [], 
        "131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d")

        self.assertEqual(self.rawInfo.index, {"https://www.example.com":
        {"text":"A", 
        "links":[], 
        "hash":"131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d"}})

        self.assertEqual(self.rawInfo.url_to_be_updated, set())
    
    def test_save_to_database(self):
        self.rawInfo.url_to_be_updated = {"https://example.com", "https://example.org","https://fortesting.com"}
        self.rawInfo.url_to_be_deleted = ["https://error.com", "https://useless.net"]
        self.testDB["RawData"].insert_one({"key":"https://error.com", "text":"dummy text", "links":{}, 
                                           "hash":"e22d73ad754cfaecee5599a91a1308fda20e32eeb5d1e243dc6404473571b4c8"})
        self.testDB["RawData"].insert_one({"key":"https://useless.net", "text":"dummy text", "links":{}, 
                                           "hash":"e7955ef03eb44e079a0b0f64dad65fa5b80990bbbf7c43c8035d66f354b0bad1"})
        self.testDB["RawData"].insert_one({"key":"https://example.com", "text":"A", "links":{"0":"https://test.com"},
                                           "hash":"566eb54d9fdb158e98b085fa2685705da6151148ef731db19d8425173433847d"})
        self.testDB["RawData"].insert_one({"key":"https://example.org", "text":"B", "links":{"0":"https://test.com"},
                                           "hash":"a9a8b871e6b40e0f87c156185b67b0f3fb330a3652582cad02f02f94710a65c8"})
        self.rawInfo.index = {"https://example.com":{"text":"example text","links":["https://test.com"],
                                                     "hash":"dbce35597750c711590d9db1f4b8c448ecc91c8cdfdbc0ddea8a2e8a8c842010"},
        "https://example.org":{"text": "example text 2", "links": ["https://test.org","https://dummy.org"], 
                               "hash": "07691af247258f52b390f5225a2c421e280e7c7f5393182bea466f0c1b2f91db"},
        "https://fortesting.com":{"text":"example text 3","links":["https://test.org","https://dummy.org"], 
                                  "hash": "f0c97bb60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a2806f3"}}
        self.rawInfo.save_to_database(self.testDB)
        result = []
        for col in self.testDB["RawData"].find({},{"_id":0,"key":1,"text":1,"links":1,"hash":1}):
            col_dict = dict()
            col_dict["key"] = col["key"]
            col_dict["text"] = col["text"]
            col_dict["links"] = col["links"]
            col_dict["hash"] = col["hash"]
            result.append(col_dict)
        self.assertEqual(result,[{"key":"https://example.com","text":"example text","links":{"0":"https://test.com"},
                                    "hash":"dbce35597750c711590d9db1f4b8c448ecc91c8cdfdbc0ddea8a2e8a8c842010"},
                                    {"key":"https://example.org","text":"example text 2","links":{"0":"https://test.org","1":"https://dummy.org"},
                                    "hash":"07691af247258f52b390f5225a2c421e280e7c7f5393182bea466f0c1b2f91db"},
                                    {"key":"https://fortesting.com","text":"example text 3","links":{"0":"https://test.org","1":"https://dummy.org"},
                                    "hash":"f0c97bb60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a2806f3"}
                                    ])
    
    def test_read_from_database(self):
        self.db["RawData"].find.return_value = [
            {"key": "https://example.com", "text": "example text", "links": {0:"https://test.com"}, "hash": "12345"},
            {"key": "https://example.org", "text": "example text 2", "links": {0:"https://test.org",1:"https://dummy.org"}, "hash": "67890"}
        ]
        self.rawInfo.read_from_database(self.db)
        self.assertEqual(self.rawInfo.index, {"https://example.com":{"text":"example text","links":["https://test.com"],"hash":"12345"},
        "https://example.org":{"text": "example text 2", "links": ["https://test.org","https://dummy.org"], "hash": "67890"}})

    def test_remove_url(self):
        self.rawInfo.index = {"https://example.org":{"text": "example text 2", "links": ["https://test.org","https://dummy.org"], 
                               "hash": "07691af247258f52b390f5225a2c421e280e7c7f5393182bea466f0c1b2f91db"},
                               "https://fortesting.com":{"text":"example text 3","links":["https://test.org","https://dummy.org"], 
                                "hash": "f0c97bb60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a2806f3"}}
        self.rawInfo.remove_urls(["https://example.org"])
        assert(self.rawInfo.index == {"https://fortesting.com":{"text":"example text 3","links":["https://test.org","https://dummy.org"], 
                                        "hash": "f0c97bb60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a2806f3"}})
        assert(self.rawInfo.url_to_be_deleted == ["https://example.org"])
    
class TestInvertedIndex(unittest.TestCase):
    
    def setUp(self):
        self.ivi = InvertedIndex()
        self.testDB = MongoClient('localhost:27017')["TestSearchEngine"]
        
    def tearDown(self):
        self.testDB.drop_collection("WebDB")
        
    def test_modify_case1(self):
        tokens = ["banana","รถยนต์","banana"]
        url = "www.testcase01.com"
        result = self.ivi.modify_index_with_tokens(tokens,[],url)
        self.assertEqual(result,{"banana":{"www.testcase01.com":2},"รถยนต์":{"www.testcase01.com":1}})
        self.assertEqual(self.ivi.keywords_to_be_updated, {"banana","รถยนต์"})
        
    def test_modify_case2(self):
        self.ivi.index ={"key1":{"www.testcase01.com":2},"key2":{"www.testcase01.com":1}}
        tokens = ["key1","key2","key1","key2"]
        url = "www.testcase01.com"
        result = self.ivi.modify_index_with_tokens(tokens,[],url)
        self.assertEqual(result,{"key1":{"www.testcase01.com":2},"key2":{"www.testcase01.com":2}})
        self.assertEqual(self.ivi.keywords_to_be_updated, {"key2"})
        
    def test_modify_case3(self):
        self.ivi.index ={"key1":{"www.testcase01.com":2},"key2":{"www.testcase01.com":1}}
        tokens = ["key1","key2","key3"]
        url = "www.testcase02.com"
        result = self.ivi.modify_index_with_tokens(tokens,[],url)
        self.assertEqual(result,{"key1":{"www.testcase01.com":2,"www.testcase02.com":1},
                                 "key2":{"www.testcase01.com":1,"www.testcase02.com":1},"key3":{"www.testcase02.com":1}})
        self.assertEqual(self.ivi.keywords_to_be_updated, {"key1","key2","key3"})
    
    def test_savetodatabase_case1(self):
        self.ivi.keywords_to_be_updated = {"key1","key2"}
        self.ivi.index = {"key1":{"www.testcase01.com":2},"key2":{"www.testcase01.com":2}}
        self.ivi.save_to_database(self.testDB)
        result = []
        for col in self.testDB["WebDB"].find({},{"_id":0,"key":1,"value":1}):
            col_dict = dict()
            col_dict["key"] = col["key"]
            col_dict["value"] = col["value"]
            result.append(col_dict)
        self.assertEqual(result,[{"key":"key1","value":{"www.testcase01.com":2}},{"key":"key2","value":{"www.testcase01.com":2}}])
        
if __name__ == "__main__":
    unittest.main()