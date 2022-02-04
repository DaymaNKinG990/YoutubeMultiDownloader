import sys
import os
import os.path
import ctypes
from main_ui import MainUi
from youtube_thread import YouTubeThread
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QApplication


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ru.daymanking.desktop.app')


class YouTubeMultiDownloader(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.__init_ui()
        self.urls = None
        self.path = None
        self.thread_pool = QThreadPool()
        self.counter = 0

    def __init_ui(self) -> None:
        self.ui = MainUi(self)
        self.ui.folder_opt.setTextMargins(20, 0, 0, 0)
        self.ui.folder_btn.clicked.connect(self.get_directory)
        self.ui.download_btn.clicked.connect(self.run_multi_downloads)
        self.show()

    def __get_urls_from_form(self) -> None:
        self.urls = self.ui.youtube_urls.toPlainText().split('\n')

    def get_directory(self) -> None:
        path_to_dir = str(QFileDialog.getExistingDirectory(self, "Select folder")).replace('/', '\\')
        self.path = path_to_dir
        self.ui.folder_opt.setText(path_to_dir)

    def update_output(self, text_res: str, num_res: int) -> None:
        self.counter += num_res
        if self.counter == len(self.urls):
            self.__enable_buttons()
        newest_text = self.ui.youtube_opt.toPlainText()
        if newest_text == '':
            newest_text += text_res
        else:
            newest_text = newest_text + '\n' + text_res
        self.ui.youtube_opt.setText(newest_text)

    def is_internet_enable(self, exception_log: str, file_name: str) -> None:
        os.remove(os.path.join(self.path, file_name))
        QtWidgets.QMessageBox.critical(self, 'Critical', exception_log)
        self.__enable_buttons()

    def __run_threads(self) -> None:
        for url in self.urls:
            yt_thread = YouTubeThread()
            yt_thread.init_args(url, self.path)
            yt_thread.signals.thread_result.connect(self.update_output)
            yt_thread.signals.error_occured.connect(self.is_internet_enable)
            self.thread_pool.start(yt_thread)

    def __enable_buttons(self) -> None:
        self.ui.download_btn.setStyleSheet("background-color: rgb(175, 0, 0);\n"
                                           "border: 1px solid #000000;\n"
                                           "border-radius: 30;\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "font: 75 14pt \"Leelawadee UI\";")
        self.ui.folder_btn.setStyleSheet("background-color: rgb(175, 0, 0);\n"
                                         "border: 1px solid #000000;\n"
                                         "border-radius: 30;\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "font: 75 14pt \"Leelawadee UI\";")
        self.ui.youtube_urls.setReadOnly(False)
        self.ui.folder_btn.setEnabled(True)
        self.ui.download_btn.setEnabled(True)

    def __disable_buttons(self) -> None:
        self.ui.download_btn.setStyleSheet("background-color: rgb(135, 0, 0);\n"
                                           "border: 1px solid #000000;\n"
                                           "border-radius: 30;\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "font: 75 14pt \"Leelawadee UI\";")
        self.ui.folder_btn.setStyleSheet("background-color: rgb(135, 0, 0);\n"
                                         "border: 1px solid #000000;\n"
                                         "border-radius: 30;\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "font: 75 14pt \"Leelawadee UI\";")
        self.ui.youtube_urls.setReadOnly(True)
        self.ui.folder_btn.setEnabled(False)
        self.ui.download_btn.setEnabled(False)

    def run_multi_downloads(self) -> None:
        if self.path is None:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'You should select a folder!')
        elif len(self.ui.youtube_urls.toPlainText()) == 0:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'You should enter/paste youtube link(s)!')
        elif any([False for url in self.ui.youtube_urls.toPlainText().split('\n') if 'youto' not in url]):
            QtWidgets.QMessageBox.warning(self, 'Warning', 'You should enter/paste youtube link(s)! Not a words.')
        else:
            self.__disable_buttons()
            self.__get_urls_from_form()
            self.__run_threads()


if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon('yt.ico'))
    application = YouTubeMultiDownloader()
    sys.exit(app.exec())
