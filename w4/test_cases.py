from general_scrape_test_w4 import Spider, Index
from bs4 import BeautifulSoup
import unittest
from unittest.mock import patch

class Index_test(unittest.TestCase):
    def test_index_init(self):
        assert Index().index == {}

    def test_start_index_with_tokens(self):
        self.assertEqual(Index().modify_index_with_tokens(["she", "ate", "a", "dog", "he", "ate", "a", "cat"], "test"),
                        {"she":["test"], "ate":["test"], "a":["test"], "dog":["test"], "he":["test"], "cat":["test"]})

    def test_start_index_with_tokens_with_punctuations(self):
        self.assertEqual(Index().modify_index_with_tokens(["she", "ate", "a", "dog", ".", "he", "ate", "a", "cat", "!", "?"], "test"),
                        {"she":["test"], "ate":["test"], "a":["test"], "dog":["test"], "he":["test"], "cat":["test"]})

class Spider_test(unittest.TestCase):

    @patch("general_scrape_test_w4.Spider.queue", new=list())
    def test_spider_init(self):
        scraper = Spider("https://www.dummy.com")
        assert scraper.url == "https://www.dummy.com"
        assert Spider.queue == ["https://www.dummy.com"]

    @patch("general_scrape_test_w4.Spider.queue", new=["https://www.test.co.th"])
    def test_spider_init_with_existing_queue(self):
        scraper = Spider("https://www.dummy.com")
        assert scraper.url == "https://www.dummy.com"
        assert Spider.queue == ["https://www.test.co.th", "https://www.dummy.com"]
    
    def test_generate_soup(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.text = "<!DOCTYPE html><html><body><h1> This is a blank HTML page </h1></body></html>"
            scraper = Spider("https://www.test.com")
            scraper.generate_soup("https://www.dummy.com")
            assert scraper.url == "https://www.dummy.com"
            assert scraper.soup == BeautifulSoup(mock_get.return_value.text, "html.parser")

    @patch("general_scrape_test_w4.Spider.queue", new=list())
    @patch("general_scrape_test_w4.Spider.get_links", return_value = {"https://www.test.co.th","https://www.dummy.com"})
    def test_add_links_to_queue(self, mock_get_links):
        scraper = Spider("https://www.not_used.com")
        scraper.add_links_to_queue()
        assert sorted(Spider.queue) == sorted(["https://www.test.co.th", "https://www.dummy.com", "https://www.not_used.com"])

    @patch("general_scrape_test_w4.Spider.queue", new=["https://Softdev.co.th", "https:Softdev.co.th/Help/me"])
    @patch("general_scrape_test_w4.Spider.get_links", return_value = {"https://www.test.co.th","https://www.dummy.com"})
    def test_add_links_to_exsiting_queue(self, mock_get_links):
        scraper = Spider("https://www.not_used.com")
        scraper.add_links_to_queue()
        assert sorted(Spider.queue) == sorted(["https://Softdev.co.th", "https:Softdev.co.th/Help/me", "https://www.test.co.th", "https://www.dummy.com", "https://www.not_used.com"])

if __name__ == "__main__" :
    unittest.main()