from Spider import Spider
from Index import Index, ReferenceIndex
from pythainlp import word_tokenize
import concurrent.futures
import threading
import time

def generate_and_crawl(spider:Spider, index:Index, ref:ReferenceIndex, thread_num:int, crawl_lock:threading.Lock, index_lock:threading.Lock):
    try:
        url = Spider.queue[Spider.queue_front]
        assert spider.generate_soup(url)
    except: return

    crawl_lock.acquire()
    text, links = spider.crawl()
    print("Thread",thread_num,"URL in queue:", len(Spider.queue) - Spider.queue_front,"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")
    crawl_lock.release()

    tokens = word_tokenize(text)

    index_lock.acquire()
    index.modify_index_with_tokens(tokens, url)
    ref.add_info_entry(url, spider.get_base_domain(url), links)
    index_lock.release()

def main(index:Index, ref:ReferenceIndex):
    crawl_lock = threading.Lock()
    index_lock = threading.Lock()
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    generate_and_crawl(spider, index, ref, 1, crawl_lock, index_lock)
    spider_nest = [Spider() for i in range(7)]
    spider_nest.append(spider)
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while Spider.queue_front != len(Spider.queue):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(len(spider_nest)):
                executor.submit(generate_and_crawl, spider_nest[i], index, ref, i+1, crawl_lock, index_lock)

if __name__ == "__main__":
    index = Index()
    ref_index = ReferenceIndex()
    start = time.time()
    main(index, ref_index)
    index.save_to_file()
    ref_index.convert_info_to_index()
    print(ref_index.ref_info)
    ref_index.save_to_file()
    stop = time.time()
    print(stop-start)