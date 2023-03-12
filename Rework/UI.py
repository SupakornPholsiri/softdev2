import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem
from IndexV2 import Index, RawInfoIndex, Database
from Tokenize import Tokenize
from Searcher import Search

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Search Bar Example")
        self.setGeometry(100, 100, 800, 600)

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create search bar and buttons
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        self.graph_button = QPushButton("Graph Spatial")
        self.graph_frequency_button = QPushButton("Graph Frequency")

        # Create toolbar and buttons
        self.toolbar = self.addToolBar("Toolbar")
        self.add_website_button = self.toolbar.addAction("Add Website")
        self.remove_website_button = self.toolbar.addAction("Remove Website")
        self.update_website_button = self.toolbar.addAction("Update Website")
        self.pause_button = self.toolbar.addAction("Pause")

        # Create layout for search bar and buttons
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.graph_button)
        self.search_layout.addWidget(self.graph_frequency_button)

        # Create list widget to display search results
        self.list_widget = QListWidget()

        # Create layout for main widget
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addWidget(self.list_widget)

        # Set main widget layout
        self.main_widget.setLayout(self.main_layout)

        self.db = Database(SearchEngine="ForSpiderTest")

        self.tokenizer = Tokenize()

        self.searcher = Search()
        
        self.raw_index = RawInfoIndex()
        self.raw_index.read_from_database(self.db)

        self.index = Index()
        self.index.read_fw_index_from_database(self.db)
        self.index.read_ivi_index_from_database(self.db)

    def search(self):
        self.list_widget.clear()

        query = self.search_bar.text()
        query_tokens = self.tokenizer.tokenize(query)
        query_tokens = self.tokenizer.filter(query_tokens)

        results = self.searcher.search(query_tokens, self.raw_index.index, self.index.fw_index, self.index.ivi_index)
        self.list_widget.addItems([result[0] for result in results])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

