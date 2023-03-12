import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem
from IndexV2 import Index, RawInfoIndex, Database
from Tokenize import Tokenize
from Searcher import Search
from MapPlot import MapPlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Noomle")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create search bar and buttons
        self.create_search_bar()
        self.create_search_button()
        self.create_spatial_graph_button()
        self.create_frequency_graph_button()

        # Create toolbar and buttons
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        add_website_button = toolbar.addAction( "Add Website")
        remove_website_button = toolbar.addAction( "Remove Website")
        update_website_button = toolbar.addAction( "Update Website")
        pause_button = toolbar.addAction( "Pause")

        # Create status bar and label
        status_bar = QStatusBar()
        status_label = QLabel("Ready")
        status_bar.addWidget(status_label)


        # Create layout for search bar and buttons
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.spatial_graph_button)
        self.search_layout.addWidget(self.frequency_graph_button)

        # Create list widget to display search results
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget::item {padding: 10px;}")
        self.list_widget.itemDoubleClicked.connect(self.on_list_widget_item_double_clicked)

        # Create layout for main widget
        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.list_widget)

        # Set main widget layout
        main_widget.setLayout(main_layout)

        # Set status bar
        self.setStatusBar(status_bar)

    def on_list_widget_item_double_clicked(self, item):
        print(item.text())


        self.index = Index()
        self.index.read_fw_index_from_database(self.db)
        self.index.read_ivi_index_from_database(self.db)

        self.mapplot = MapPlot()

    def create_search_bar(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter a search term")
        self.search_bar.setMinimumWidth(200)

    def create_search_button(self):
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: #0078d7; color: white;")
        self.search_button.clicked.connect(self.search)

    def create_spatial_graph_button(self):
        self.spatial_graph_button = QPushButton("Spatial Graph")
        self.spatial_graph_button.setStyleSheet("background-color: #0078d7; color: white;")
        self.spatial_graph_button.clicked.connect(self.spatial_graph)

    def create_frequency_graph_button(self):
        self.frequency_graph_button = QPushButton("Graph Frequency")
        self.frequency_graph_button.setStyleSheet("background-color: #0078d7; color: white;")
        self.frequency_graph_button.clicked.connect(self.frequency_graph)
    
    def search(self):
        self.list_widget.clear()

        query = self.search_bar.text()
        query_tokens = self.tokenizer.tokenize(query)
        query_tokens = self.tokenizer.filter(query_tokens)
        results = self.searcher.search(query_tokens, self.raw_index.index, self.index.fw_index, self.index.ivi_index)

        self.list_widget.addItems([result[0] for result in results])
        self.statusBar().showMessage(f"Found {len(results)} results.")

    def spatial_graph(self):
        pass

    def frequency_graph(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

