from Spider import Spider
from Index import Index
from pythainlp import word_tokenize
import time

def main(index:Index):
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while Spider.queue_front != len(Spider.queue):
        url = Spider.queue[Spider.queue_front]
        spider.generate_soup(url)
        text = spider.crawl()
        tokens = word_tokenize(text)
        index.modify_index_with_tokens(tokens, url)
        print("URL in queue:", len(Spider.queue) - Spider.queue_front,"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")

if __name__ == "__main__":
    index = Index()
    start = time.time()
    main(index)
    index.save_to_file()
    stop = time.time()
    print(stop-start)