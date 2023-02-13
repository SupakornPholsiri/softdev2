from Spider import Spider
from Index import Index, ReferenceIndex
from pythainlp import word_tokenize
import time

def main(index:Index, ref_index:ReferenceIndex):
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while Spider.queue_front != len(Spider.queue):
        url = Spider.queue[Spider.queue_front]
        spider.generate_soup(url)
        text, links = spider.crawl()
        tokens = word_tokenize(text)
        index.modify_index_with_tokens_no_mongo(tokens, url)
        ref_index.add_info_entry(url, spider.get_base_domain(url), links)
        print("URL in queue:", len(Spider.queue) - Spider.queue_front,"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")

if __name__ == "__main__":
    index = Index()
    ref_index = ReferenceIndex()
    start = time.time()
    main(index, ref_index)
    index.save_to_file()
    ref_index.convert_info_to_index()
    ref_index.save_to_file()
    stop = time.time()
    print(stop-start)