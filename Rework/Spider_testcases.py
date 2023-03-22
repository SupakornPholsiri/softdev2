import unittest
from unittest.mock import patch, MagicMock
from SpiderV2 import Spider
import requests
from bs4 import BeautifulSoup

class Spider_testcases(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        Spider.queue = []
        Spider.crawled = []
        Spider.queue_front = 0
        Spider.depth = 0
        Spider.max_depth = 2

    @patch.object(Spider, "queue", new = [])
    @patch.object(Spider, "crawled", new = [])
    def test_init(self):
        spider = Spider("https://www.softdev.com")
        assert Spider.queue == ["https://www.softdev.com"]

    @patch.object(Spider, "queue", new = ["https://www.softdev.com"])
    @patch.object(Spider, "crawled", new = [])
    def test_init_with_existing_url_in_queue(self):
        spider = Spider("https://www.w4buniversity.com")
        assert Spider.queue == ["https://www.softdev.com", "https://www.w4buniversity.com"]

    @patch.object(Spider, "queue", new = ["https://www.w4buniversity.com"])
    @patch.object(Spider, "crawled", new = [])
    def test_init_with_duplicate_in_queue(self):
        spider = Spider("https://www.w4buniversity.com")
        assert Spider.queue == ["https://www.w4buniversity.com"]

    @patch.object(Spider, "queue", new = ["https://www.w4buniversity.com", "https://www.dummy.com"])
    @patch.object(Spider, "crawled", new = ["https://www.crawled.com"])
    def test_init_with_duplicate_in_queue2(self):
        spider = Spider("https://www.w4buniversity.com")
        assert Spider.queue == ["https://www.w4buniversity.com", "https://www.dummy.com"]

    @patch.object(Spider, "queue", new = [])
    @patch.object(Spider, "crawled", new = ["https://www.nescafe.co.th"])
    def test_init_with_duplicate_crawled(self):
        spider = Spider("https://www.nescafe.co.th")
        assert Spider.queue == []

    @patch.object(Spider, "queue", new = ["https://www.freerobux.com", "https://www.freeiphone.com"])
    @patch.object(Spider, "crawled", new = ["https://www.traveloga.co.th","https://www.nescafe.co.th"])
    def test_init_with_duplicate_crawled2(self):
        spider = Spider("https://www.nescafe.co.th")
        assert Spider.queue == ["https://www.freerobux.com", "https://www.freeiphone.com"]

    @patch.object(Spider, "queue", new = [])
    @patch.object(Spider, "crawled", new = [])
    def test_init_no_url(self):
        spider = Spider()
        assert Spider.queue == []

    @patch.object(Spider, "queue", new = ["https://www.placeholder.com"])
    @patch.object(Spider, "crawled", new = [])
    def test_init_no_url_with_existing_in_queue(self):
        spider = Spider()
        assert Spider.queue == ["https://www.placeholder.com"]

    def test_get_text(self):
        spider = Spider("https://www.unittest.com")
        spider.soup = BeautifulSoup("<!DOCTYPE html><html><body><h1>This is a</h1><p>blank HTML page</p></body></html>", "html.parser")
        assert spider.get_text() == "  this is a blank html page"

    def test_get_base_domain(self):
        assert Spider.get_base_domain("https://test.com") == "test.com"
        assert Spider.get_base_domain("https://www.example.com/testing") == "www.example.com"

    def test_change_depth(self):
        Spider.queue_front = 2
        Spider.queue_back = 1
        Spider.depth = 0
        Spider.max_depth = 2
        assert Spider.try_change_depth()
        
    def test_not_changing_depth(self):
        Spider.queue_front = 1
        Spider.queue_back = 1
        Spider.depth = 0
        Spider.max_depth = 2
        assert not Spider.try_change_depth()

    def test_max_depth(self):
        Spider.queue_front = 2
        Spider.queue_back = 1
        Spider.depth = 2
        Spider.max_depth = 2
        assert not Spider.try_change_depth()


    """@patch.object(Spider, "get_links", return_value = {"https://www.unittest.com", "https://www.test.com", "http://www.unit.com"})
    def test_add_links_to_queue(self, mock_get_links):
        spider = Spider("https://www.unittest.com")
        spider.url = "https://www.unittest.com"
        spider.add_links_to_queue()
        assert sorted(Spider.queue) == sorted(["http://www.unit.com", "https://www.unittest.com", "https://www.test.com"])

    @patch.object(Spider, "get_links", return_value = {"https://www.unittest.com", "https://www.test.com", "http://www.unit.com"})
    @patch.object(Spider, "crawled", new = ["https://www.test.com"])
    def test_add_links_to_queue_with_duplicate_in_crawled_or_current_url(self, mock_get_links):
        spider = Spider("https://www.unittest.com")
        spider.url = "https://www.unit.com"
        spider.add_links_to_queue()
        assert sorted(Spider.queue) == sorted(["http://www.unit.com", "https://www.unittest.com"])      
"""
if __name__ == "__main__":
    unittest.main()