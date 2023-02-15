from pythainlp import word_tokenize
import emoji
import re

test = "Yesasdasdasd Baby Study Studying studied 😀 D-13216546541323D หัวเราะนะครับ"
class Tokenize:
    def __init__(self) -> None:
         self.tokens = ""
    def tokenize(self,tokens):
        re1 = re.sub("[0-9]|[+\-*/]|[\t\n]"," ",tokens)
        # tokens = re.findall(r'\b\w+\b', re1)
        # print(tokens)
        afteremoji = ""
        for i in re1:
            if i in emoji.EMOJI_DATA:
                afteremoji += " "
            else:
                afteremoji += i
        tokenized = word_tokenize(afteremoji)
        finaltokenized = []
        for x in tokenized:
            if x.startswith(" ") or x == "\xa0":
                continue
            else:
                finaltokenized.append(x)
        return finaltokenized

if __name__ == "__main__":
    ex = Tokenize()
    print(ex.tokenize(test))


    

        
        