from Spider import Spider
import concurrent.futures

def main():
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while Spider.queue_front != len(Spider.queue):
        spider.generate_soup(Spider.queue[Spider.queue_front])
        spider.crawl()
        print("URL in queue:", len(Spider.queue) - Spider.queue_front,"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")

if __name__ == "__main__":
    main()