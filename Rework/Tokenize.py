from pythainlp import word_tokenize
import emoji
import re
from nltk.stem import WordNetLemmatizer
import nltk
class Tokenize:
    def tokenize(self,tokens):
        """Receive String user Regular Expression filter special character and unnecessary character"""
        re1 = re.sub(r'[][!-@#|{}\\$?%+:"\n^_\t]'," ",tokens)
        afteremoji = ""
        """Filter Emoji"""
        for i in re1:
            if i in emoji.EMOJI_DATA:
                afteremoji += " "
            else:
                afteremoji += i
        tokenized = word_tokenize(afteremoji)
        finaltokenized = []
        lemmatizer = WordNetLemmatizer()
        """Filter empty list"""
        for x in tokenized:
            if x.startswith(" ") :
                continue
            else:
                finaltokenized.append(lemmatizer.lemmatize(x))
        return finaltokenized
    def filter(self,inputlist):
        """Filter 1 character"""
        result = []
        for c in inputlist:
            if len(c) == 1:
                continue
            else:
                result.append(c)
        return result
    


    

        
        