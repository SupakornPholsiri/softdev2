from IndexV2 import Index, RawInfoIndex, Database
from Tokenize import Tokenize
from Searcher import Search
from MapPlot import MapPlot
from SpiderV2 import Spider

from UI2 import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QUrl

class SpatialGraphThread(QThread):
    done_signal = pyqtSignal()

    def __init__(self, results):
        super().__init__()
        self.results = results
        self.locations = {}

    def run(self):
        # Compute location frequencies
        for result in self.results :
            for loc in result[3]:
                if loc in self.locations:
                    self.locations[loc] += 1
                else:
                    self.locations[loc] = 1

        # Generate map plot
        mapplot = MapPlot()
        mapplot.getMapPlot(self.locations)
        self.done_signal.emit()

class ScrapeThread(QThread):
    web_scraped_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, root_urls:list, raw_index:RawInfoIndex, index:Index, tokenizer:Tokenize, db:Database):
        super().__init__()
        self.root_urls = root_urls.copy()
        self.raw_index = raw_index
        self.index = index
        self.tokenizer = tokenizer
        self.db = db

    def run(self):
        Spider.queue = self.root_urls
        Spider.crawled = []
        Spider.unaccessible_urls = []
        Spider.base_domains = []
        Spider.set_base_domains(self.root_urls)
        Spider.queue_front = 0
        Spider.queue_back = len(Spider.queue)
        Spider.depth = 0

        spider = Spider()
        while Spider.queue_front != len(Spider.queue):
            print(Spider.queue[Spider.queue_front], Spider.queue_front)
            try:
                url = Spider.queue[Spider.queue_front]
                assert spider.generate_next_soup()

                if url in self.raw_index.index:
                    hash_in_storage = self.raw_index.index[url]["hash"]
                else:
                    hash_in_storage = None
                data = spider.crawl(hash_in_storage)
                if data :
                    raw_text, links, hash = data

                    text = self.tokenizer.tokenize(raw_text)
                    text = self.tokenizer.filter(text)
                
                    self.raw_index.modify_index(url, raw_text, links, hash)
                    self.web_scraped_signal.emit(f"URLs in queue: {len(Spider.queue) - Spider.queue_front} | URLs crawled: {len(Spider.crawled)} | Scraped {spider.url}")
                else:
                    pass
                
            except AssertionError:
                pass
        self.raw_index.remove_urls(Spider.unaccessible_urls)
        self.raw_index.save_to_database(self.db)
        for url in self.raw_index.index:
            tokens = self.tokenizer.tokenize(self.raw_index.index[url]["text"])
            tokens = self.tokenizer.filter(tokens)
            tokens = self.tokenizer.make_counter(tokens)
            self.index.remove_urls(self.raw_index.url_to_be_deleted)
            self.index.modify_index(url, tokens)
        self.web_scraped_signal.emit("Saving to database...")
        self.index.remove_urls(self.raw_index.url_to_be_deleted)
        self.index.save_fw_index_to_database(self.db)
        self.index.save_ivi_index_to_database(self.db)
        self.done_signal.emit()       

class AppMainWindow(MainWindow):
    def __init__(self):
        super().__init__()

        self.root_urls = ["https://iot-kmutnb.github.io/blogs"]

        self.cached_query = ""
        self.cached_spatial_query = ""
        self.cached_graph_query = ""
        self.results = []

        self.db = Database(SearchEngine="ForSpiderTest")

        self.tokenizer = Tokenize()

        self.searcher = Search()
        
        self.raw_index = RawInfoIndex()
        self.raw_index.read_from_database(self.db)

        self.index = Index()
        self.index.read_fw_index_from_database(self.db)
        self.index.read_ivi_index_from_database(self.db)

        self.search_button.clicked.connect(self.search)
        self.spatial_graph_button.clicked.connect(self.spatial_graph)

        self.scrape_begin_button.clicked.connect(self.scrape)

    def search(self):
        if self.cached_query == self.search_bar.text():
            self.stacked_widget.setCurrentWidget(self.list_widget)
        else:
            self.list_widget.clear()
            self.stacked_widget.setCurrentWidget(self.list_widget)

            self.cached_query = self.search_bar.text()
            query_tokens = self.tokenizer.tokenize(self.cached_query)
            query_tokens = self.tokenizer.filter(query_tokens)
            self.results = self.searcher.search(query_tokens, self.raw_index.index, self.index.fw_index, self.index.ivi_index)

            self.list_widget.addItems([result[0] for result in self.results])
        self.statusBar().showMessage(f"Found {len(self.results)} results for {self.cached_query}.")

    def spatial_graph(self):
        self.statusBar().showMessage("Plotting...")
        if self.map == self.stacked_widget.currentWidget() or self.cached_spatial_query == self.cached_query:
            self.stacked_widget.setCurrentWidget(self.map)
            self.map.reload()
            self.statusBar().showMessage(f"Spatial Graph of {self.cached_spatial_query}.")
        else:
            self.spatial_thread = SpatialGraphThread(self.results)
            self.spatial_thread.start()
            self.spatial_thread.done_signal.connect(self.spatial_graph_done)

    def spatial_graph_done(self):
        self.spatial_thread.terminate()
        self.map.load(QUrl.fromLocalFile(r"C:\Users\supak\Documents\GitHub\softdev2\Rework\Map.html"))
        self.cached_spatial_query = self.cached_query
        self.statusBar().showMessage(f"Spatial Graph of {self.cached_spatial_query} loaded.")

    def scrape(self):
        self.statusBar().showMessage("Scraping...")
        self.scrape_thread = ScrapeThread(self.root_urls, self.raw_index, self.index, self.tokenizer, self.db)
        self.scrape_thread.web_scraped_signal.connect(self.add_scrape_status)
        self.scrape_thread.done_signal.connect(self.scrape_done)
        self.scrape_thread.start()

    def add_scrape_status(self, str):
        self.scrape_status_widget.addItem(str)

    def scrape_done(self):
        self.scrape_thread.terminate()
        self.statusBar().showMessage("Scraping done")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())