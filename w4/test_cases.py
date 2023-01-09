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
    
    def test_generate_soup(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.text = "<!DOCTYPE html><html><body><h1> This is a blank HTML page </h1></body></html>"
            scraper = Spider()
            scraper.generate_soup("https://www.dummy.com")
            assert scraper.url == "https://www.dummy.com"
            assert scraper.soup == BeautifulSoup(mock_get.return_value.text, "html.parser")

if __name__ == "__main__" :
    unittest.main()