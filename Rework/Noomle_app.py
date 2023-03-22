from IndexV2 import Index, RawInfoIndex, Database
from Tokenize import Tokenize
from Searcher import Search
from MapPlot import MapPlot
from SpiderV2 import Spider

from UI2 import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QUrl

import atexit
import time
import pickle
import os
import os.path

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
    pause_signal = pyqtSignal()
    web_scraped_signal = pyqtSignal(str)
    done_signal = pyqtSignal()
    abort_signal = pyqtSignal()
    
    def __init__(self, root_urls:list, raw_index:RawInfoIndex, index:Index, tokenizer:Tokenize, db:Database):
        super().__init__()
        self.pause = False
        self.stopped = False
        try:
            with open("saved_state.pkl", "rb") as f:
                state = pickle.load(f)
                self.root_urls = state["rooturls"].copy()
                self.raw_index = raw_index
                self.index = index
                self.tokenizer = tokenizer
                self.db = db

                Spider.queue = state["que"]
                Spider.crawled = state["crawled"]
                Spider.unaccessible_urls = state["unaccessurl"]
                Spider.base_domains = []
                Spider.set_base_domains(self.root_urls)
                Spider.queue_front = state["quef"]
                Spider.queue_back = state["queb"]
                Spider.depth = state["dep"]

                self.raw_index.url_to_be_updated = state["urltoup"]
                self.raw_index.url_to_be_deleted = state["urltodel"]
                self.raw_index.in_queue_deleted = state["inquedel"]

                self.index.urls_to_be_updated = state["indextoup"]
                self.index.urls_to_be_removed = state["indextodel"]
                self.index.urls_removed_from_database = state["indextodelfromdb"]

                self.index.keywords_to_be_updated = state["keytoup"]
                self.index.keywords_to_be_removed = state["keytodel"]
                self.index.keywords_removed_from_database = state["keytodelfromdb"]

        except FileNotFoundError:
            self.root_urls = root_urls.copy()
            self.raw_index = raw_index
            self.index = index
            self.tokenizer = tokenizer
            self.db = db

            Spider.queue = self.root_urls
            Spider.crawled = []
            Spider.unaccessible_urls = []
            Spider.base_domains = []
            Spider.set_base_domains(self.root_urls)
            Spider.queue_front = 0
            Spider.queue_back = len(Spider.queue)
            Spider.depth = 0

            self.raw_index.url_to_be_updated = set()
            self.raw_index.url_to_be_deleted = []
            self.raw_index.in_queue_deleted = 0

            self.index.urls_to_be_updated = set()
            self.index.urls_to_be_removed = []
            self.index.urls_removed_from_database = 0

            self.index.keywords_to_be_updated = set()
            self.index.keywords_to_be_removed = []
            self.index.keywords_removed_from_database = 0
        
    def run(self):
        spider = Spider()
        while Spider.queue_front != len(Spider.queue):
            print(len(Spider.queue), Spider.queue[Spider.queue_front], Spider.queue_front, Spider.queue_back, Spider.depth)
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
                
                    self.raw_index.modify_index(url, raw_text, links, hash)
                    self.web_scraped_signal.emit(f"URLs in queue: {len(Spider.queue) - Spider.queue_front} | URLs crawled: {len(Spider.crawled)} | Scraped {spider.url}")
                
                if self.stopped:
                    break
                
                if self.pause:
                    self.save_state()
                
            except AssertionError:
                pass

            while self.pause:
                time.sleep(0)

        self.web_scraped_signal.emit("Modifying index...")

        #Uncomment the code if you want the scrape to remove all url that is not found that run
        #for url in self.raw_index.get_urls():
            #if url not in Spider.queue:
                #Spider.unaccessible_urls.append(url)
            
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

        if os.path.isfile("saved_state.pkl"):
            os.remove("saved_state.pkl")

        self.done_signal.emit()

    def pause_toggle(self):
        """Pause the scraping process\n
        ******Don't pause after the final web have been scraped.******"""
        self.pause = not self.pause

    def save_state(self):
        state = {   "rooturls":self.root_urls,"que":Spider.queue,"crawled":Spider.crawled,"unaccessurl":Spider.unaccessible_urls,
                    "quef":Spider.queue_front,"queb":Spider.queue_back,"dep":Spider.depth,"urltoup":self.raw_index.url_to_be_updated,
                    "urltodel":self.raw_index.url_to_be_deleted,"inquedel":self.raw_index.in_queue_deleted,"indextoup":self.index.urls_to_be_updated,
                    "indextodel":self.index.urls_to_be_removed,"indextodelfromdb":self.index.urls_removed_from_database,
                    "keytoup":self.index.keywords_to_be_updated,"keytodel":self.index.keywords_to_be_removed,
                    "keytodelfromdb":self.index.keywords_removed_from_database}
        with open("saved_state.pkl", "wb") as f:
            pickle.dump(state, f)

    def stop(self):
        """Abort the scraping process\n
        ******Don't stop after the final web have been scraped.******"""
        self.stopped = True
        self.raw_index.read_from_database(self.db)
        if os.path.isfile("saved_state.pkl"):
            os.remove("saved_state.pkl")
        self.abort_signal.emit()

            
class AppMainWindow(MainWindow):
    def __init__(self):
        super().__init__()

        with open("root_urls.txt", "r", encoding="utf-8") as f:
            self.root_urls = f.read().splitlines() 
            f.close()
        self.cached_query = ""
        self.cached_spatial_query = ""
        self.cached_graph_query = ""
        self.results = []
        self.pause = 0
        self.url_target = ""

        self.db = Database(SearchEngine="ForSpiderTest")

        self.tokenizer = Tokenize()

        self.searcher = Search()
        
        self.raw_index = RawInfoIndex()
        self.raw_index.read_from_database(self.db)
        self.URL_list.addItems(self.raw_index.get_urls())

        self.index = Index()
        self.index.read_fw_index_from_database(self.db)
        self.index.read_ivi_index_from_database(self.db)

        self.search_button.clicked.connect(self.search)
        self.spatial_graph_button.clicked.connect(self.spatial_graph)
        self.frequency_graph_button.clicked.connect(self.bar_graph_func)

        self.scrape_begin_button.clicked.connect(self.scrape)
        self.scrape_pause_button.clicked.connect(self.handle_pause)
        self.scrape_stop_button.clicked.connect(self.handle_stop)

        self.URL_view_action.triggered.connect(self.refresh_URL_list)
        self.add_website_button.clicked.connect(self.add_root_url)
        self.remove_website_button.clicked.connect(self.remove_URL)
        self.root_URL_list.itemClicked.connect(self.change_URL_target)
        self.URL_list.itemClicked.connect(self.change_URL_target)

        self.tab_widget.currentChanged.connect(self.change_tab)

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

    def bar_graph_func(self):
        if self.bar_graph == self.stacked_widget.currentWidget():
            self.stacked_widget.setCurrentWidget(self.bar_graph)
            self.bar_graph.reload()
            self.statusBar().showMessage(f"Bar graph of {'Placeholder'}.")
        else:
            #placeholder
            self.stacked_widget.setCurrentWidget(self.bar_graph)
            self.statusBar().showMessage(f"Bar graph of {'Placeholder'} loaded.")

    def scrape(self):
        self.scrape_begin_button.setEnabled(False)
        self.statusBar().showMessage("Scraping...")
        print(self.root_urls)
        self.scrape_thread = ScrapeThread(self.root_urls, self.raw_index, self.index, self.tokenizer, self.db)
        self.scrape_thread.web_scraped_signal.connect(self.add_scrape_status)
        self.scrape_thread.done_signal.connect(self.scrape_done)
        self.scrape_thread.abort_signal.connect(self.scrape_aborted)
        self.scrape_thread.start()

    def add_scrape_status(self, str):
        self.scrape_status_widget.addItem(str)

    def scrape_done(self):
        self.scrape_thread.terminate()
        self.statusBar().showMessage("Scraping done")
        self.scrape_begin_button.setEnabled(True)

    def scrape_aborted(self):
        self.scrape_thread.terminate()
        self.raw_index.read_from_database(self.db)
        self.statusBar().showMessage("Scraping aborted")
        self.scrape_begin_button.setEnabled(True)
        self.scrape_pause_button.setText("Pause")

    def change_tab(self, index):
        if index == 2:
            self.refresh_URL_list()
    
    def add_root_url(self):
        URL_input = self.URL_input.text()
        if URL_input not in self.root_urls and URL_input != "":
            self.root_urls.append(URL_input)
        self.refresh_URL_list()

    def refresh_URL_list(self):
        self.root_URL_list.clear()
        self.URL_list.clear()
        self.root_URL_list.addItems(self.root_urls)
        self.URL_list.addItems(self.raw_index.get_urls())
        self.tab_widget.setCurrentIndex(2)
        self.statusBar().showMessage("Refreshed")

    def change_URL_target(self, item):
        print(item.text())
        self.url_target = item.text()

    def remove_URL(self):
        if self.url_target in self.root_urls or self.url_target in self.raw_index.get_urls():
            self.root_urls.remove(self.url_target)
            self.raw_index.remove_urls([self.url_target])
            self.index.remove_urls([self.url_target])
            self.raw_index.save_to_database(self.db)
            self.index.save_fw_index_to_database(self.db)
            self.index.save_ivi_index_to_database(self.db)
            self.refresh_URL_list()

    def exit_handler(self):
        with open("root_urls.txt", "w", encoding="utf-8") as f:
            for root_url in self.root_urls:
                f.write(f"{root_url}\n")
            f.close()

    def handle_pause(self):
        self.scrape_thread.pause_toggle()
        if self.scrape_pause_button.text() == "Pause":
            self.scrape_pause_button.setText("Unpause")
        else:
            self.scrape_pause_button.setText("Pause")

    def handle_stop(self):
        self.scrape_thread.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppMainWindow()
    atexit.register(window.exit_handler)
    window.show()
    sys.exit(app.exec_())