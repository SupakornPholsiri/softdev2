from pythainlp import word_tokenize
import emoji
import re
from nltk.stem import WordNetLemmatizer
from collections import Counter

class Tokenize:
    def __init__(self):
        self.stopword = self.ListOfStopword()
    
    def ListOfStopword(self):
        with open("stop_words_english.txt","r")as f:
            listsw = f.read(listsw)
            listsw = listsw.split("\n")
            return listsw
        
    def FilterStopWord(self,token):
        listtoken = []
        for i in token:
            if i in self.stopword:
                continue
            else:
                listtoken.append(token[i])
        return listtoken
    
    def tokenize(self,tokens):
        """Receive String use Regular Expression to filter special character and unnecessary character"""
        re1 = re.sub(r'[][!-@#|{}\\$?%+:"\n^_\t]'," ",tokens)
        afteremoji = ""
        """Filter Emoji"""
        for i in re1:
            if i in emoji.EMOJI_DATA:
                afteremoji += " "
            else:
                afteremoji += i
        tokenized = word_tokenize(afteremoji)
        swfilterd = self.FilterStopWord(tokenized)
        finaltokenized = []
        lemmatizer = WordNetLemmatizer()
        """Filter empty list"""
        for x in swfilterd:
            if x.startswith(" ") :
                continue
            else:
                finaltokenized.append(lemmatizer.lemmatize(x).lower())
        return finaltokenized
    
    def filter(self, inputlist):
        """Filter 1 character"""
        result = []
        for c in inputlist:
            if len(c) == 1:
                continue
            else:
                result.append(c)
        return result
    
    def make_counter(self, tokens_list:list[str]):
        """Create a counter object for the tokens"""
        return Counter(tokens_list)


    

        
        