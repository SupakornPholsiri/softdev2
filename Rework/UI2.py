import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Noomle")
        self.setGeometry(100, 100, 800, 600)

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create search bar and buttons
        self.create_search_bar()
        self.create_search_button()
        self.create_spatial_graph_button()
        self.create_frequency_graph_button()

        # Create toolbar and buttons
        self.toolbar = self.addToolBar("Toolbar")
        self.search_action = self.toolbar.addAction("Search")
        self.scrape_action = self.toolbar.addAction("Scrape")
        self.add_website_button = self.toolbar.addAction("Add Website")
        self.remove_website_button = self.toolbar.addAction("Remove Website")

        # Create layout for search bar and buttons
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.spatial_graph_button)
        self.search_layout.addWidget(self.frequency_graph_button)

        # Create list widget to display search results
        self.list_widget = QListWidget()

        # Create WebEngineView to display map
        self.map = QWebEngineView()

        # Create list widget to display scrape status
        self.scrape_status_widget = QListWidget()

        self.scrape_begin_button = QPushButton("Scrape")
        self.scrape_begin_button.setStyleSheet("background-color: #0078d7; color: white;")
        self.scrape_pause_button = QPushButton("Pause")
        self.scrape_pause_button.setStyleSheet("background-color: #0078d7; color: white;")
        self.scrape_stop_button = QPushButton("Stop")
        self.scrape_stop_button.setStyleSheet("background-color: #0078d7; color: white;")

        self.scrape_option = QHBoxLayout()
        self.scrape_option.addWidget(self.scrape_begin_button)
        self.scrape_option.addWidget(self.scrape_pause_button)
        self.scrape_option.addWidget(self.scrape_stop_button)

        self.scrape_layout = QVBoxLayout()
        self.scrape_layout.addLayout(self.scrape_option)
        self.scrape_layout.addWidget(self.scrape_status_widget)

        # Create stacked widget to switch between search results and map views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.list_widget)
        self.stacked_widget.addWidget(self.map)

        self.statusBar().showMessage("Test")

        # Create layout for main widget
        self.search_results_widget = QVBoxLayout()
        self.search_results_widget.addLayout(self.search_layout)
        self.search_results_widget.addWidget(self.stacked_widget)

        self.search_widget = QWidget()
        self.search_widget.setLayout(self.search_results_widget)

        self.scrape_widget = QWidget()
        self.scrape_widget.setLayout(self.scrape_layout)

        # Create tab widget to switch between search results and scrape status
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.search_widget, "Search Results")
        self.tab_widget.addTab(self.scrape_widget, "Scrape Status")

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)

        # Set main widget layout
        self.main_widget.setLayout(self.main_layout)

        # Connect actions to methods
        self.search_action.triggered.connect(self.show_search_results)
        self.scrape_action.triggered.connect(self.show_scrape_status)

    def create_search_bar(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter a search term")
        self.search_bar.setMinimumWidth(200)

    def create_search_button(self):
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: #0078d7; color: white;")

    def create_spatial_graph_button(self):
        self.spatial_graph_button = QPushButton("Spatial Graph")
        self.spatial_graph_button.setStyleSheet("background-color: #0078d7; color: white;")

    def create_frequency_graph_button(self):
        self.frequency_graph_button = QPushButton("Graph Frequency")
        self.frequency_graph_button.setStyleSheet("background-color: #0078d7; color: white;")

    def show_search_results(self):
        self.tab_widget.setCurrentIndex(0)

    def show_scrape_status(self):
        self.tab_widget.setCurrentIndex(1)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())