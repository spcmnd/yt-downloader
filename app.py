from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from pytube import YouTube


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
        self.main_title = QLabel('Please enter URL:', self)
        self.main_title.setStyleSheet('font-weight: bold;')
        self.main_title.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.main_title)

    def init_url_input(self):
        self.url_input = QLineEdit()
        self.url_input.setStyleSheet(
            'width: 400px; border-radius: 4px; border: 1px solid black; padding: 4px;')
        self.main_layout.addWidget(self.url_input)

    def init_download_button(self):
        self.download_button = QPushButton('Download', self)
        self.download_button.setStyleSheet(
            'background-color: red; color: white; font-weight: bold;')
        self.download_button.clicked.connect(self.handle_download)
        self.main_layout.addWidget(self.download_button)

    def handle_download(self):
        url = self.url_input.text()

        try:
            yt = YouTube(url, on_complete_callback=self.on_download_complete)
            yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download()
        except:
            self.toggle_result_message(True)

    def on_download_complete(self, stream, file_path):
        self.url_input.setText('')
        self.toggle_result_message(False)

    def toggle_result_message(self, is_error):
        if hasattr(self, 'result_message'):
            self.main_layout.removeWidget(self.result_message)

        if is_error == True:
            message = 'An error occurred.'
            colorStyle = 'color: red;'
        else:
            message = 'Video downloaded.'
            colorStyle = 'color: green;'

        self.result_message = QLabel(message)
        self.result_message.setStyleSheet(colorStyle)
        self.main_layout.addWidget(self.result_message)


if __name__ == '__main__':
    app = QApplication([])
    main = Window()
    app.exec()
