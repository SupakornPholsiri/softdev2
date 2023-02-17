from pythainlp import word_tokenize
import emoji
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
class Tokenize:
    def tokenize(self,tokens):
        """จะรับ Tokens มาเเบบเป็นข้อความยาวเป็น String เเล้วนำมาใช้ re.sub เป็นการใช้ Regular Expression
            โดย sub นี้จะเอาพวกตัวเลข สัญลักษณ์พิเศษออก เเล้วเเทนที่ด้วย String ว่าง"""
        re1 = re.sub(r'[][!-@#|{}\\$?%+:"\n^_\t]'," ",tokens)
        afteremoji = ""
        """จะเป็นการกรองเอา emoji ออก โดยนำ Library emoji มาใช้ โดยจะให้ลูปเทียบกับลิสต์ emoji ที่ import เข้ามา เเล้วเทนที่ด้วย String ว่าง"""
        for i in re1:
            if i in emoji.EMOJI_DATA:
                afteremoji += " "
            else:
                afteremoji += i
        """หลังจากผ่านลูมาเเล้วจะได้เป็นก่อนข้อความจะทำการใช้ Tokenize อย่างง่ายของ NLTK ได้ผลลัพธ์เป็นลิสต์ที่เป็นคำๆ"""
        tokenized = word_tokenize(afteremoji)
        finaltokenized = []
        lemmatizer = WordNetLemmatizer()
        """เป็นขั้นตอนสุดจะกรองเอาลิสต์ที่เป็น String ว่างออกไปให้หมดเเล้วทำการ Lemmatize ด้วย เเล้วส่งผลลัพธ์กลับเป็นลิสต์ใหม่"""
        for x in tokenized:
            if x.startswith(" ") :
                continue
            else:
                finaltokenized.append(lemmatizer.lemmatize(x))
        return finaltokenized
    def filter(self,inputlist):
        """เป็นฟังก์ชั่นไว้กรองพวกข้อความที่มีตัวอักษรเดียว ซึ่งไม่มีประโยชน์ต่อการหาข้อมูลจะทำการเอาออกเเล้วส่งผลลัพธ์กลับเป็นลิสต์ใหม่"""
        result = []
        for c in inputlist:
            if len(c) == 1:
                continue
            else:
                result.append(c)
        return result
    


    

        
        