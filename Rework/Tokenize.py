from pythainlp import word_tokenize
import emoji
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
class Tokenize:
    
    def tokenize(self,tokens):
        re1 = re.sub(r'[][!-@#$?%+:"\n^_]'," ",tokens)
        afteremoji = ""
        for i in re1:
            if i in emoji.EMOJI_DATA:
                afteremoji += " "
            else:
                afteremoji += i
        tokenized = word_tokenize(afteremoji)
        finaltokenized = []
        lemmatizer = WordNetLemmatizer()
        for x in tokenized:
            if x.startswith(" ") :
                continue
            else:
                finaltokenized.append(lemmatizer.lemmatize(x))
        return finaltokenized
    def filter(self,inputlist):
        result = []
        for c in inputlist:
            if len(c) == 1:
                continue
            else:
                result.append(c)
        return result
    


    

        
        