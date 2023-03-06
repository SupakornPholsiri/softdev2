import unittest
from unittest.mock import patch, Mock, MagicMock, call
import mongomock
from IndexV2 import RawInfoIndex, InvertedIndex, Index
from pymongo import MongoClient
from collections import Counter
class RawInfoTest(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()
        self.db.raw_data_storage = MagicMock()
        self.rawInfo = RawInfoIndex()
        self.testDB = MongoClient('localhost:27017')["TestSearchEngine"]
        self.testDB.raw_data_storage = self.testDB["RawData"]

    def tearDown(self):
        self.testDB.drop_collection("RawData")
    
    def test_init(self):
        assert self.rawInfo.index == {}
        assert self.rawInfo.url_to_be_updated == set()
        assert self.rawInfo.url_to_be_deleted == []
        assert self.rawInfo.in_queue_deleted == 0

    def test_get_urls(self):
        self.rawInfo.index = {"https://www.example.com":
        {"text":"A",
        "links":[],
        "hash":"131410cd33081dcb5ffc7d22e75ce424f1cd7f4db053d3a401ae0a864ca5b66d"},
        "https://www.test.com":
        {"text":"B",
        "links":["https://www.dummy.com"],
        "hash":"8ce2c05fc4d1d4beb81ab0e25cb606b26e5ffcb090b7fe08187760ff74c1db63"}}

        assert self.rawInfo.get_urls() == ["https://www.example.com","https://www.test.com"]

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
        "A \nB\tC", 
        ["https://www.dummy.com"], 
        "8ce2c05fc4d1d4beb81ab0e25cb606b26e5ffcb090b7fe08187760ff74c1db63")

        self.assertEqual(self.rawInfo.index, {"https://www.example.com":
        {"text":"A B C", 
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
        self.assertEqual(self.rawInfo.in_queue_deleted, 2)
    
    def test_read_from_database(self):
        self.db.raw_data_storage.find.return_value = [
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

    def test_get_ref_count(self):
        self.rawInfo.index = {  "https://example.org":{"text": "example text 2", "links": ["https://test.org","https://fortesting.com"], 
                                "hash": "07691af247258f52b390f5225a2c421e280e7c7f5393182bea466f0c1b2f91db"},
                                "https://fortesting.com":{"text":"example text 3","links":["https://test.org","https://dummy.org"], 
                                "hash": "f0c97bb60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a2806f3"},
                                "https://test.org":{"text":"example text 4","links":["https://test.org","https://dummy.org"], 
                                "hash": "a42fg9b60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a23464d"},
                                "https://test.org/signal":{"text":"example text 4","links":["https://test.org","https://example.org"], 
                                "hash": "a42fg9b60ae0305a7393534e27c54f5f23e0894fd35a380a459f87015a23464d"}}
        assert self.rawInfo.get_ref_count("https://test.org") == 2
        assert self.rawInfo.get_ref_count("https://example.org") == 1
        assert self.rawInfo.get_ref_count("https://fortesting.com") == 1
        assert self.rawInfo.get_ref_count("https://test.org/signal") == 0
        assert self.rawInfo.get_ref_count("https://dummy.org") == 0
    
class TestInvertedIndex(unittest.TestCase):
    
    testDB = MongoClient('localhost:27017')["TestSearchEngine"]
    testDB.dbweb = testDB["WebDB"]
    
    def setUp(self):
        self.db = MagicMock()
        self.db.dbweb = MagicMock()
        self.ivi = InvertedIndex()
        
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
        self.testDB["WebDB"].insert_one({"key":"key1","value":{"www.existing.com":3}})
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
        
    def test_read_from_database(self):
        self.db.dbweb.find.return_value = [
            {"key":"word1","value":{"www.test01.com":1}},{"key":"word2","value":{"www.test02.com":2}}]
        self.ivi.read_from_database(self.db)
        self.assertEqual(self.ivi.index, {"word1":{"www.test01.com":1},"word2":{"www.test02.com":2}})

class TestIndex(unittest.TestCase):

    testDB = MongoClient('localhost:27017')["TestSearchEngine"]
    testDB.dbweb = testDB["WebDB"]
    testDB.fw_index = testDB["FWIndex"]
    
    def setUp(self):
        self.index = Index()

    def tearDown(self):
        self.testDB.drop_collection("FWIndex")
        self.testDB.drop_collection("WebDB")

    @patch("IndexV2.Index.modify_ivi_index")
    def test_remove_urls(self, mock_modify):
        self.index.fw_index = {"https://www.software.com":{"Keywords":{"software":5, "innovation":2},"Location":{}},
                               "https://www.burnedout.net":{"Keywords":{"burn":4, "engineer":2},"Location":{}},
                               "https://www.kmutnb.ac.th":{"Keywords":{"engineer":5, "innovation":1},"Location":{}}}
        self.index.remove_urls(["https://www.software.com", "https://www.burnedout.net"])

        assert self.index.fw_index == {"https://www.kmutnb.ac.th":{"Keywords":{"engineer":5, "innovation":1},"Location":{}}}
        self.assertCountEqual(mock_modify.call_args_list,
                              [call([],"*","https://www.software.com",),call([],"*","https://www.burnedout.net",)])
    
    @patch("IndexV2.Index.find_missing_keywords_in_url")
    @patch("IndexV2.Index.modify_ivi_index")
    @patch("IndexV2.Index.modify_fw_index")
    def test_modify_index(self, mock_modify_fw, mock_modify_ivi, mock_missing_keywords):
        base_domains = ["https://www.software.com","https://www.burnedout.net","https://www.kmutnb.ac.th"]
        self.index.modify_index("https://www.software.com",["software","innovation"])

        mock_missing_keywords.assert_called_once_with("https://www.software.com",["software","innovation"])
        mock_modify_ivi.assert_called_once_with(["software","innovation"], mock_missing_keywords(), "https://www.software.com")
        mock_modify_fw.assert_called_once_with("https://www.software.com",["software","innovation"])

    def test_remove_url_from_all_keywords(self):
        self.index.ivi_index = {"software":{"https://www.software.com":5},
                                "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                "burn":{"https://www.burnedout.net":4},
                                "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        self.index.remove_url_from_keywords("https://www.burnedout.net","*")

        assert self.index.ivi_index ==  {"software":{"https://www.software.com":5},
                                        "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                        "engineer":{"https://www.kmutnb.ac.th":5}}
        
        assert self.index.keywords_to_be_updated == {"engineer"}
        assert self.index.keywords_to_be_removed == ["burn"]
        
    def test_remove_url_from_keywords(self):
        self.index.ivi_index = {"software":{"https://www.software.com":5},
                                "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                "burn":{"https://www.burnedout.net":4},
                                "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        self.index.remove_url_from_keywords("https://www.burnedout.net",["engineer"])

        assert self.index.ivi_index ==  {"software":{"https://www.software.com":5},
                                        "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                        "burn":{"https://www.burnedout.net":4},
                                        "engineer":{"https://www.kmutnb.ac.th":5}}
        
        assert self.index.keywords_to_be_updated == {"engineer"}
        assert self.index.keywords_to_be_removed == []

    def test_remove_url_from_keywords_2(self):
        self.index.ivi_index = {"software":{"https://www.software.com":5},
                                "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                "burn":{"https://www.burnedout.net":4},
                                "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        self.index.remove_url_from_keywords("https://www.software.com",["software"])
        self.index.remove_url_from_keywords("https://www.software.com",["burn"])
        self.index.remove_url_from_keywords("https://www.test.com",["innovation","engineer"])

        assert self.index.ivi_index ==  {"innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                        "burn":{"https://www.burnedout.net":4},
                                        "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        
        assert self.index.keywords_to_be_updated == set()
        assert self.index.keywords_to_be_removed == ["software"]

    def test_find_missing_keywords_in_url(self):
        self.index.fw_index = {"https://www.software.com":{"Keywords":{"software":5, "innovation":2},"Location":{}},
                               "https://www.burnedout.net":{"Keywords":{"burn":4, "engineer":2},"Location":{}},
                               "https://www.kmutnb.ac.th":{"Keywords":{"engineer":5, "innovation":1},"Location":{}}}
        missing = self.index.find_missing_keywords_in_url("https://www.software.com",Counter({"software":5,"renovation":2}))
        assert missing == {"innovation"}

    @patch("IndexV2.Index.remove_url_from_keywords")
    def test_modify_ivi_index(self, mock_remove_url):
        self.index.ivi_index = {"software":{"https://www.software.com":5},
                                "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                "burn":{"https://www.burnedout.net":4},
                                "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        
        self.index.modify_ivi_index(Counter({"hardware":3,"software":4}),[],"https://www.testcase01.com")
        self.index.modify_ivi_index(Counter({"innovation":3}),[],"https://www.kmutnb.ac.th")

        assert self.index.ivi_index == {"software":{"https://www.software.com":5,"https://www.testcase01.com":4},
                                        "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":3},
                                        "burn":{"https://www.burnedout.net":4},
                                        "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5},
                                        "hardware":{"https://www.testcase01.com":3}}
        
        assert self.index.keywords_to_be_updated == {"hardware","software","innovation"}

    @patch("IndexV2.Index.remove_url_from_keywords")
    def test_modify_ivi_index_call_for_removal(self, mock_remove_url):
        self.index.ivi_index = {"software":{"https://www.software.com":5},
                                "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                "burn":{"https://www.burnedout.net":4},
                                "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        self.index.modify_ivi_index(Counter({"innovation":3}),["engineer"],"https://www.kmutnb.ac.th")
        mock_remove_url.assert_called_once_with("https://www.kmutnb.ac.th",["engineer"])

    def test_get_location_info(self):
        self.index.locations = ["thailand","england","germany"]
        location = self.index.get_location_info({"thailand":3, "best":1, "germany":2})
        assert location == {"thailand":3,"germany":2}
        
    @patch("IndexV2.Index.get_location_info", return_value = {"thailand":2})
    def test_modify_fw_index(self, mock_location):
        self.index.fw_index = {"https://www.software.com/home":{"Keywords":{"software":5, "innovation":2},"Location":{}},
                               "https://www.burnedout.net/":{"Keywords":{"burn":4, "engineer":2},"Location":{}},
                               "https://www.kmutnb.ac.th/":{"Keywords":{"engineer":5, "innovation":1},"Location":{}}}
        self.index.modify_fw_index("https://www.software.com/home",{"software":5, "innovation":2, "thailand":2})
        self.index.modify_fw_index("https://www.software.com/blogs",{"blogs":5, "software":7, "thailand":2})
        assert self.index.fw_index == { "https://www.software.com/home":{"Keywords":{"software":5, "innovation":2, "thailand":2},"Location":{"thailand":2}},
                                        "https://www.burnedout.net/":{"Keywords":{"burn":4, "engineer":2},"Location":{}},
                                        "https://www.kmutnb.ac.th/":{"Keywords":{"engineer":5, "innovation":1},"Location":{}},
                                        "https://www.software.com/blogs":{"Keywords":{"blogs":5, "software":7, "thailand":2},"Location":{"thailand":2}}}
        
    def test_save_ivi_index_to_database(self):
        self.index.keywords_to_be_updated = {"software", "burn", "engineer", "fire"}
        self.index.keywords_to_be_removed = ["nothing"]
        self.testDB.dbweb.insert_one({"key":"software", "value":{"https://www.software.com":5, "https://www.notexist.com":7}})
        self.testDB.dbweb.insert_one({"key":"innovation", "value":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1}})
        self.testDB.dbweb.insert_one({"key":"burn", "value":{"https://www.burnedout.net":5}})
        self.testDB.dbweb.insert_one({"key":"engineer", "value":{"https://www.burnedout.net":7,"https://www.dpis.ac.th":5}})
        self.testDB.dbweb.insert_one({"key":"nothing", "value":{"https://www.notexist.com":10}})
        self.index.ivi_index = {"software":{"https://www.software.com":5},
                                "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                "burn":{"https://www.burnedout.net":4},
                                "engineer":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5},
                                "fire":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}
        self.index.save_ivi_index_to_database(self.testDB)
        result = []
        for col in self.testDB.dbweb.find({},{"_id":0,"key":1,"value":1}):
            col_dict = dict()
            col_dict["key"] = col["key"]
            col_dict["value"] = col["value"]
            result.append(col_dict)
        self.assertCountEqual(result,[{"key":"software", "value":{"https://www.software.com":5}},
                                 {"key":"innovation", "value":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1}},
                                 {"key":"burn", "value":{"https://www.burnedout.net":4}},
                                 {"key":"engineer", "value":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}},
                                 {"key":"fire", "value":{"https://www.burnedout.net":2,"https://www.kmutnb.ac.th":5}}])
        assert self.index.keywords_to_be_updated == set()
        assert self.index.keywords_removed_from_database == 1

    def test_read_ivi_index_from_database(self):
        self.testDB.dbweb.insert_one({"key":"software", "value":{"https://www.software.com":5, "https://www.notexist.com":7}})
        self.testDB.dbweb.insert_one({"key":"innovation", "value":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1}})
        self.testDB.dbweb.insert_one({"key":"burn", "value":{"https://www.burnedout.net":5}})
        self.testDB.dbweb.insert_one({"key":"engineer", "value":{"https://www.burnedout.net":7,"https://www.dpis.ac.th":5}})
        self.index.read_ivi_index_from_database(self.testDB)
        assert self.index.ivi_index == {"software":{"https://www.software.com":5, "https://www.notexist.com":7},
                                        "innovation":{"https://www.software.com":2,"https://www.kmutnb.ac.th":1},
                                        "burn":{"https://www.burnedout.net":5},
                                        "engineer":{"https://www.burnedout.net":7,"https://www.dpis.ac.th":5}}
        
    def test_save_fw_index_to_database(self):
        self.index.urls_to_be_updated = {"https://www.software.com/home","https://www.burnedout.net/"}
        self.index.urls_to_be_removed = ["https://www.dealerhaven.com/threads"]
        self.testDB.fw_index.insert_one({"key":"https://www.software.com/home", "value":{"Keywords":{"software":5, "innovation":2},"Location":{}}})
        self.testDB.fw_index.insert_one({"key":"https://www.dealerhaven.com/threads", "value":{"Keywords":{"deal":5, "discount":2, "russia":4},"Location":{"russia":4}}})
        self.testDB.fw_index.insert_one({"key":"https://www.kmutnb.ac.th/", "value":{"Keywords":{"engineer":5, "innovation":1, "thailand":3, "germany":5},"Location":{"thailand":3, "germany":5}}})
        self.index.fw_index = {"https://www.software.com/home":{"Keywords":{"software":5, "innovation":2, "thailand":2},"Location":{"thailand":2}},
                               "https://www.burnedout.net/":{"Keywords":{"burn":4, "engineer":2, "england":1, "egypt":4},"Location":{"england":1, "egypt":4}},
                               "https://www.kmutnb.ac.th/":{"Keywords":{"engineer":5, "innovation":1, "thailand":3, "germany":5},"Location":{"thailand":3, "germany":5}}}
        self.index.save_fw_index_to_database(self.testDB)
        result = []
        for col in self.testDB.fw_index.find({},{"_id":0,"key":1,"value":1}):
            col_dict = dict()
            col_dict["key"] = col["key"]
            col_dict["value"] = col["value"]
            result.append(col_dict)
        self.assertCountEqual(result, [{"key":"https://www.software.com/home", "value":{"Keywords":{"software":5, "innovation":2, "thailand":2},"Location":{"thailand":2}}},
                                       {"key":"https://www.kmutnb.ac.th/", "value":{"Keywords":{"engineer":5, "innovation":1, "thailand":3, "germany":5},"Location":{"thailand":3, "germany":5}}},
                                       {"key":"https://www.burnedout.net/", "value":{"Keywords":{"burn":4, "engineer":2, "england":1, "egypt":4},"Location":{"england":1, "egypt":4}}}])
        assert self.index.urls_to_be_updated == set()
        assert self.index.urls_removed_from_database == 1

    def test_read_fw_index_from_database(self):
        self.testDB.fw_index.insert_one({"key":"https://www.software.com/home", "value":{"Keywords":{"software":5, "innovation":2},"Location":{}}})
        self.testDB.fw_index.insert_one({"key":"https://www.dealerhaven.com/threads", "value":{"Keywords":{"deal":5, "discount":2, "russia":4},"Location":{"russia":4}}})
        self.testDB.fw_index.insert_one({"key":"https://www.kmutnb.ac.th/", "value":{"Keywords":{"engineer":5, "innovation":1, "thailand":3, "germany":5},"Location":{"thailand":3, "germany":5}}})
        self.index.read_fw_index_from_database(self.testDB)
        assert self.index.fw_index == {"https://www.software.com/home":{"Keywords":{"software":5, "innovation":2},"Location":{}},
                                       "https://www.dealerhaven.com/threads":{"Keywords":{"deal":5, "discount":2, "russia":4},"Location":{"russia":4}},
                                       "https://www.kmutnb.ac.th/":{"Keywords":{"engineer":5, "innovation":1, "thailand":3, "germany":5},"Location":{"thailand":3, "germany":5}}}
if __name__ == "__main__":
    unittest.main()