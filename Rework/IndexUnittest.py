import unittest
from unittest.mock import patch, MagicMock
from mongomock import MongoClient
from IndexV2 import RawInfoIndex
from pymongo import MongoClient

class RawInfoTest(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()
        self.rawInfo = RawInfoIndex()
    
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

    @patch.object(MongoClient,"my_collection")
    def test_save_to_database(self, mock_collection):
        pass
    
    def test_read_from_database(self):
        self.db["RawData"].find.return_value = [
            {"key": "https://example.com", "text": "example text", "links": {0:"https://test.com"}, "hash": "12345"},
            {"key": "https://example.org", "text": "example text 2", "links": {0:"https://test.org",1:"https://dummy.org"}, "hash": "67890"}
        ]
        self.rawInfo.read_from_database(self.db)
        self.assertEqual(self.rawInfo.index, {"https://example.com":{"text":"example text","links":["https://test.com"],"hash":"12345"},
        "https://example.org":{"text": "example text 2", "links": ["https://test.org","https://dummy.org"], "hash": "67890"}})

    def test_remove_url(self):
        self.rawInfo.index = {"A":{},"B":{}}
        self.rawInfo.remove_urls(["A"])
        assert(self.rawInfo.index == {"B":{}})
        assert(self.rawInfo.url_to_be_deleted == ["A"])

if __name__ == "__main__":
    unittest.main()