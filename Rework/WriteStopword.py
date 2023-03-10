from pythainlp.corpus import thai_stopwords
with open("stop_words_english.txt",'a',encoding="utf-8") as f:
    for i in thai_stopwords():
        f.write(f"{i}\n")
    f.close()