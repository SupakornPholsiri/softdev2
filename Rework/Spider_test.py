from SpiderV2 import Spider
from IndexV2 import RawInfoIndex, Index, Database
from Tokenize import Tokenize

import concurrent.futures
import threading
import time

db = Database(SearchEngine="ForSpiderTest")
raw_storage = RawInfoIndex()
raw_storage.read_from_database(db)
tokenizer = Tokenize()

def generate_and_crawl(spider:Spider, raw_index:RawInfoIndex, thread_num:int, crawl_lock:threading.Lock, index_lock:threading.Lock):
    try:
        url = Spider.queue[Spider.queue_front]
        assert spider.generate_next_soup()
    except: return

    crawl_lock.acquire()
    if url in raw_storage.index:
        hash_in_storage = raw_storage.index[url]["hash"]
    else:
        hash_in_storage = None
    data = spider.crawl(hash_in_storage)
    if data :
        raw_text, links, hash = data
    else:
        return
    print("Thread",thread_num,"URL in queue:", len(Spider.queue) - Spider.queue_front,"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")
    crawl_lock.release()

    text = tokenizer.tokenize(raw_text)
    text = tokenizer.filter(text)
    counter = tokenizer.make_counter(text)

    index_lock.acquire()
    raw_index.modify_index(url, raw_text, links, hash)
    index_lock.release()

def main(raw_index:RawInfoIndex):
    crawl_lock = threading.Lock()
    index_lock = threading.Lock()
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    Spider.set_base_domains(["https://iot-kmutnb.github.io/"])
    Spider.max_depth = 3
    generate_and_crawl(spider, raw_index, 1, crawl_lock, index_lock)
    spider_nest = [Spider() for i in range(7)]
    spider_nest.append(spider)
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while Spider.queue_front != len(Spider.queue):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(len(spider_nest)):
                executor.submit(generate_and_crawl, spider_nest[i], raw_index, i+1, crawl_lock, index_lock)

if __name__ == "__main__":
    start = time.time()
    main(raw_storage)
    raw_storage.save_to_database(db)
    stop = time.time()
    print(stop-start)