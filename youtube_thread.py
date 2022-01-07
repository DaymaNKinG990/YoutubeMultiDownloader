from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot
from pytube import YouTube


class YouTubeThreadSignals(QtCore.QObject):
    thread_result = QtCore.pyqtSignal(str, int)
    error_occured = QtCore.pyqtSignal(str, str)


class YouTubeThread(QtCore.QRunnable):

    def __init__(self) -> None:
        super().__init__()
        self.youtube = YouTube
        self.url = None
        self.path = None
        self.is_video = None
        self.signals = YouTubeThreadSignals()

    def __download_video(self) -> None:
        local_yt = self.youtube(url=self.url)
        hq = local_yt.streams.get_highest_resolution()
        if hq.exists_at_path(file_path=self.path):
            self.signals.thread_result.emit(f'Video \"{local_yt.title}\" has been downloaded already!', 1)
        else:
            try:
                hq.download(output_path=self.path, timeout=15)
                self.signals.thread_result.emit(f'Video \"{local_yt.title}\" has been downloaded successfully!', 1)
            except:
                self.signals.error_occured.emit('Internet connection is lost. Retry later.', f'{local_yt.title}')

    def __download_audio(self) -> None:
        local_yt = self.youtube(url=self.url)
        hq = local_yt.streams.get_audio_only()
        if hq.exists_at_path(file_path=self.path):
            self.signals.thread_result.emit(f'Audio \"{local_yt.title}\" has been downloaded already!', 1)
        else:
            try:
                hq.download(output_path=self.path, timeout=15)
                self.signals.thread_result.emit(f'Audio \"{local_yt.title}\" has been downloaded successfully!', 1)
            except:
                self.signals.error_occured.emit('Internet connection is lost. Retry later.', f'{local_yt.title}')

    def init_args(self, url: str, path: str = None, video: bool = True) -> None:
        self.url = url
        self.path = path
        self.is_video = video

    @pyqtSlot()
    def run(self) -> None:
        if self.is_video:
            self.__download_video()
        else:
            self.__download_audio()
