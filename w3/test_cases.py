from general_scrape_test2 import Scraper, Index
import unittest

class Index_test(unittest.TestCase):
    def test_index_init(self):
        assert Index().index == {}

    def test_start_index_with_tokens(self):
        self.assertEqual(Index().modify_index_with_tokens(["she", "ate", "a", "dog", "he", "ate", "a", "cat"], "test"),
                        {"she":["test"], "ate":["test"], "a":["test"], "dog":["test"], "he":["test"], "cat":["test"]})

    def test_start_index_with_tokens_with_punctuations(self):
        self.assertEqual(Index().modify_index_with_tokens(["she", "ate", "a", "dog", ".", "he", "ate", "a", "cat", "!", "?"], "test"),
                        {"she":["test"], "ate":["test"], "a":["test"], "dog":["test"], "he":["test"], "cat":["test"]})

if __name__ == "__main__" :
    unittest.main()