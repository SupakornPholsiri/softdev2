import unittest
from unittest.mock import patch
from Spider import Spider
import requests
from bs4 import BeautifulSoup

class Spider_testcases(unittest.TestCase):

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
        
    @patch.object(requests, "get")
    @patch.object(Spider, "get_base_domain", return_value = "https://www.yummyyapper.com")
    def test_generate_soup(self, mock_base_domain, mock_get):
        mock_get.return_value.text = "<!DOCTYPE html><html><body><h1> This is a blank HTML page </h1></body></html>"
        spider = Spider("https://www.yummyyapper.com/menu/sweet")
        spider.generate_soup("https://www.yummyyapper.com/menu/sweet")
        assert spider.url == "https://www.yummyyapper.com/menu/sweet"
        assert spider.base_domain == "https://www.yummyyapper.com"
        assert spider.soup == BeautifulSoup("<!DOCTYPE html><html><body><h1> This is a blank HTML page </h1></body></html>", "html.parser")

if __name__ == "__main__":
    unittest.main()