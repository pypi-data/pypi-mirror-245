from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QColor, QMovie
from PySide6.QtWidgets import QLabel
from ..core import WidgetBase
import os


class MovieView(WidgetBase, QLabel):
    def __init__(self,
                 *,
                 filename: str = None,
                 bg_color: QColor = None,
                 scale_size: QSize = None,
                 speed: int = None,
                 running: bool = False,
                 **kwargs):
        QLabel.__init__(self)
        super().__init__(**kwargs)

        if (QByteArray(bytes(
            os.path.basename(filename).split(".")[-1].lower(), "utf-8")) 
            not in QMovie.supportedFormats()):
            raise ValueError("invalid filename, unsupported format!")

        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._movie = QMovie(self)

        if filename is not None:
            self._movie.setFileName(filename)

        if bg_color is not None:
            self._movie.setBackgroundColor(bg_color)

        if scale_size is not None:
            self._movie.setScaledSize(scale_size)

        if speed is not None:
            self._movie.setSpeed(speed)

        if running:
            self._movie.start()

        self.setMovie(self._movie)
