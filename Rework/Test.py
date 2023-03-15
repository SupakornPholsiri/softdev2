import sys
from PyQt5.QtWidgets import QComboBox,QLabel,QToolBar,QStyleFactory,QAction,QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

            # Set window properties
        self.setWindowTitle("Search Bar Example")
        self.setGeometry(100, 100, 800, 600)

        # Set window style to Fusion
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create search bar and buttons
        search_bar = QLineEdit()
        search_button = QPushButton("Search")
        graph_button = QPushButton("Graph Spatial")
        graph_frequency_button = QPushButton("Graph Frequency")

        # Create toolbar and buttons
        toolbar = QToolBar("Toolbar")
        toolbar.setMovable(False)
        add_website_action = QAction(self.style().standardIcon(getattr(QStyleFactory, 'SP_FileDialogNewFolder')), "Add Website", self)
        remove_website_action = QAction(self.style().standardIcon(getattr(QStyleFactory, 'SP_DialogDiscardButton')), "Remove Website", self)
        update_website_action = QAction(self.style().standardIcon(getattr(QStyleFactory, 'SP_FileDialogContentsView')), "Update Website", self)
        pause_action = QAction(self.style().standardIcon(getattr(QStyleFactory, 'SP_MediaPause')), "Pause", self)
        toolbar.addActions([add_website_action, remove_website_action, update_website_action, pause_action])
        self.addToolBar(toolbar)

        # Create dropdown menu to sort results
        sort_label = QLabel("Sort by:")
        sort_combo = QComboBox()
        sort_combo.addItems(["Relevance", "Date", "Rating"])

        # Create layout for search bar and buttons
        search_layout = QHBoxLayout()
        search_layout.addWidget(search_bar)
        search_layout.addWidget(search_button)
        search_layout.addWidget(graph_button)
        search_layout.addWidget(graph_frequency_button)
        search_layout.addStretch(1)
        search_layout.addWidget(sort_label)
        search_layout.addWidget(sort_combo)

        # Create list widget to display search results
        self.list_widget = QListWidget()

        # Create layout for main widget
        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.list_widget)

        # Set main widget layout
        main_widget.setLayout(main_layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
