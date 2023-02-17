import unittest
from unittest.mock import patch,mock_open
from Tokenize import Tokenize

#Test Tokenize
class Test(unittest.TestCase):
    
    def test_Tokenize_1stcase(self):
        #เคสตัวอักษรอังกฤษ 1
        Tokenizer = Tokenize()
        test1 = "crying cry cries"
        self.assertEqual(Tokenizer.tokenize(test1),["cry","cry","cry"])
    def test_Tokenize_2ndcase(self):
        #เคสตัวอักษณอังกฤษ 2
        Tokenizer = Tokenize()
        test1 = "Crying crying cried"
        self.assertEqual(Tokenizer.tokenize(test1),["Crying","cry","cried"])
    def test_Tokenize_3rdcase(self):
        #เคส Emoji
        Tokenizer = Tokenize()
        test1 = "It is really 😙👌"
        self.assertEqual(Tokenizer.tokenize(test1),["It","is","really"])
    def test_Tokenize_4thcase(self):
        #เคสภาษาไทยรวมกับอังกฤษ
        Tokenizer = Tokenize()
        test1 = "Oh Baby Baby อู้ โว้ว"
        self.assertEqual(Tokenizer.tokenize(test1),["Oh","Baby","Baby","อู้","โว้ว"])
    def test_Tokenize_5thcase(self):
        #เคสรวม Emoji ไทย เเละอังกฤษ
        Tokenizer = Tokenize()
        test1 = "Oh Baby Baby อู้ โว้ว โจ้ว โจ้ว เอิ้บ 🙌 🙌 🙌 🙌"
        self.assertEqual(Tokenizer.tokenize(test1),["Oh","Baby","Baby","อู้","โว้ว","โจ้ว","โจ้ว","เอิ้บ"])
    def test_Tokenize_6thcase(self):
        #เคสตัวอักษรพิเศษ
        Tokenizer = Tokenize()
        test1 = "I▶you"
        self.assertEqual(Tokenizer.tokenize(test1),["I","you"])
    def test_Tokenize_7thcase(self):
        #เคส Punctuation
        Tokenizer = Tokenize()
        test1 = "Banana-cupcake"
        self.assertEqual(Tokenizer.tokenize(test1),["Banana","cupcake"])
        
        
    def test_Tokenizefilter_1stcase(self):
        #เคสภาษาอังกฤษ
        Tokenizer = Tokenize()
        test1 = ["It","s","really","nice"]
        self.assertEqual(Tokenizer.filter(test1),["It","really","nice"])
    def test_Tokenizefilter_2stcase(self):
        #เคสภาษาไทย
        Tokenizer = Tokenize()
        test1 = ["กู","บ","เป็น","หยัง"]
        self.assertEqual(Tokenizer.filter(test1),["กู","เป็น","หยัง"])
    def test_Tokenizefilter_3stcase(self):
        #เคสรวมไทย อังกฤษ
        Tokenizer = Tokenize()
        test1 = ["กู","บ","เป็น","หยัง","I","a","Okay","นะ","ยู","โนว"]
        self.assertEqual(Tokenizer.filter(test1),["กู","เป็น","หยัง","Okay","นะ","ยู","โนว"])
        
        
        
if __name__ == '__main__':
    unittest.main()
        