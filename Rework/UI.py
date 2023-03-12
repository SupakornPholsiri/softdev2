import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QToolBar, QStatusBar, QLabel, QComboBox, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
            # Set window properties
        self.setWindowTitle("Search Bar Example")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create search bar and buttons
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Enter a search term")
        search_bar.setMinimumWidth(200)
        search_button = QPushButton("Search")
        search_button.setStyleSheet("background-color: #0078d7; color: white;")
        graph_button = QPushButton("Graph Spatial")
        graph_button.setStyleSheet("background-color: #0078d7; color: white;")
        graph_frequency_button = QPushButton("Graph Frequency")
        graph_frequency_button.setStyleSheet("background-color: #0078d7; color: white;")

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
        search_layout = QHBoxLayout()
        search_layout.addWidget(search_bar)
        search_layout.addWidget(search_button)
        search_layout.addWidget(graph_button)
        search_layout.addWidget(graph_frequency_button)

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

