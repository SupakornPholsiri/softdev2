from Spider import Spider
import concurrent.futures
import threading
import time

def generate_and_crawl(spider:Spider, thread_num:int, crawl_lock:threading.Lock):
    try:
        url = Spider.queue[Spider.queue_front]
        assert spider.generate_soup(url)
    except: return

    crawl_lock.acquire()
    text, links, hash = spider.crawl()
    print("Thread",thread_num,"URL in queue:", len(Spider.queue) - Spider.queue_front,"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")
    
    crawl_lock.release()

def main():
    crawl_lock = threading.Lock()
    spider = Spider("https://riskofrain.fandom.com")
    spider.set_base_domains(["https://www.riskofrain.com", "https://riskofrain.fandom.com", "https://riskofrain2.fandom.com"])
    generate_and_crawl(spider, 1, crawl_lock)
    spider_nest = [Spider() for i in range(7)]
    spider_nest.append(spider)
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while Spider.queue_front != len(Spider.queue):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(len(spider_nest)):
                executor.submit(generate_and_crawl, spider_nest[i], i+1, crawl_lock)
    

if __name__ == "__main__":
    start = time.time()
    main()
    stop = time.time()
    print(stop-start)