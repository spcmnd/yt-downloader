from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.window.setWindowTitle('YT Downloader')
        self.init_main_layout()
        self.window.show()
    
    def init_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.init_main_title()
        self.init_url_input()
        self.init_download_button()
        self.window.setLayout(self.main_layout)
    
    def init_main_title(self):
        self.main_title = QLabel('YT Downloader')
        self.main_layout.addWidget(self.main_title)

    def init_url_input(self):
        self.url_input = QLineEdit()
        self.main_layout.addWidget(self.url_input)

    def init_download_button(self):
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.handle_download)
        self.main_layout.addWidget(self.download_button)
    
    def handle_download(self):
        print(self.url_input.text())


if __name__ == '__main__':
    app = QApplication([])
    main = Window()
    app.exec()
