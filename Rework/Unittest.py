import unittest
from unittest.mock import patch,mock_open
from Tokenize import Tokenize

#Test Tokenize
class Test(unittest.TestCase):
    def test_Tokenize_1stcase(self):
        #ENG 1
        Tokenizer = Tokenize()
        test1 = "crying cry cries"
        self.assertEqual(Tokenizer.tokenize(test1),["cry","cry","cry"])
    def test_Tokenize_2ndcase(self):
        #ENG 2
        Tokenizer = Tokenize()
        test1 = "Crying crying cried"
        self.assertEqual(Tokenizer.tokenize(test1),["Crying","cry","cried"])
    def test_Tokenize_3rdcase(self):
        #Emoji
        Tokenizer = Tokenize()
        test1 = "It is really 😙👌"
        self.assertEqual(Tokenizer.tokenize(test1),["It","is","really"])
    def test_Tokenize_4thcase(self):
        #Thai-ENG
        Tokenizer = Tokenize()
        test1 = "Test ไทย"
        self.assertEqual(Tokenizer.tokenize(test1),["Test","ไทย"])
    def test_Tokenize_5thcase(self):
        #Emoji Thai ENG
        Tokenizer = Tokenize()
        test1 = "Hands ยกมือ 🙌 🙌 🙌 🙌"
        self.assertEqual(Tokenizer.tokenize(test1),["Hands","ยกมือ"])
    def test_Tokenize_6thcase(self):
        #Special Character
        Tokenizer = Tokenize()
        test1 = "I▶you!-@#$?%+:;^_<>=*{}()&/|\t\n\\"
        self.assertEqual(Tokenizer.tokenize(test1),["I","you"])
    def test_Tokenize_7thcase(self):
        #Punctuation
        Tokenizer = Tokenize()
        test1 = "Banana-cupcake"
        self.assertEqual(Tokenizer.tokenize(test1),["Banana","cupcake"])
    def test_Tokenizefilter_1stcase(self):
        #ENG
        Tokenizer = Tokenize()
        test1 = ["It","s","really","nice"]
        self.assertEqual(Tokenizer.filter(test1),["It","really","nice"])
    def test_Tokenizefilter_2stcase(self):
        #Thai
        Tokenizer = Tokenize()
        test1 = ["ข้า","บ","เป็น","หยัง"]
        self.assertEqual(Tokenizer.filter(test1),["ข้า","เป็น","หยัง"])
    def test_Tokenizefilter_3stcase(self):
        #Thai-ENG
        Tokenizer = Tokenize()
        test1 = ["ท","ท","ไทย","T","Test"]
        self.assertEqual(Tokenizer.filter(test1),["ไทย","Test"])
        
if __name__ == '__main__':
    unittest.main()
        