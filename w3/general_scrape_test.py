import requests
from bs4 import BeautifulSoup
import re
import pythainlp
import pythainlp.util

def crawl(url, index = {}):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    links_html = soup.find_all("a", href = True)
    links = set()
    for link_html in links_html:
        print(link_html['href'])
        if link_html['href'].startswith("//"):
            links.add(f'https:{link_html["href"]}')
        elif link_html['href'].startswith("/"):
            links.add(f'{"".join(url.split("/")[0:3])}{link_html["href"]}')
        else:
            links.add(link_html['href'])
    print(links)
    
    text = soup.text.lower()
    text = re.sub(r"[?,<>\[\]()\s_\|]"," ",text)
    for word in text.split():
        if pythainlp.util.countthai(word) != 0:
            for i in pythainlp.word_tokenize(word, engine = 'newmm'):
                if not i:
                    continue
                if i not in index:
                    index[i] = [url]
                elif url not in index[i]:
                    index[i].append(url)
            continue
        if not word:
            continue
        if word not in index:
            index[word] = [url]
        elif url not in index[word]:
            index[word].append(url)

    return index

urls = ["https://thairath.co.th"]
index = {}
for url in urls:
    index.update(crawl(url))

print(index.keys())
