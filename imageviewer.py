from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel
)

class ImageViewer(QWidget):
    def __init__(self, imgs, time = 500):
        super(ImageViewer, self).__init__()
        self.setWindowTitle("1")
        self.width = 900
        self.height = 900
        self.images = imgs

        height, width, channel = imgs[0].shape
        qimg = QImage(
            imgs[0].data, width, height, 3 * width, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg).scaled(
            self.width, self.height, Qt.KeepAspectRatio
        )
        self.label = QLabel()
        self.label.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(time)
        self.index = 1

    def run(self):
        if self.index != len(self.images):
            height, width, channel = self.images[self.index].shape
            qimg = QImage(
                self.images[self.index].data,
                width,
                height,
                3 * width,
                QImage.Format_RGB888,
            ).rgbSwapped()
            pixmap = QPixmap.fromImage(qimg).scaled(
                self.width, self.height, Qt.KeepAspectRatio
            )
            self.label.setPixmap(pixmap)
            self.setWindowTitle(str(self.index + 1))
            self.index += 1

class ImageViewer2(QWidget):
    def __init__(self, img1, img2):
        super(ImageViewer2, self).__init__()
        self.setWindowTitle("Result")
        self.width = 900
        self.height = 900

        grid = QGridLayout()
        grid.addWidget(QLabel("Distorted Image"), 0, 0)
        grid.addWidget(QLabel("Undistorted Image"), 0, 1)
        self.label1 = QLabel()
        height, width, channel = img1.shape
        qimg = QImage(
            img1.data, width, height, 3 * width, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg).scaled(
            self.width, self.height, Qt.KeepAspectRatio
        )
        self.label1.setPixmap(pixmap)
        
        self.label2 = QLabel()
        height, width, channel = img2.shape
        qimg = QImage(
            img2.data, width, height, 3 * width, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg).scaled(
            self.width, self.height, Qt.KeepAspectRatio
        )
        self.label2.setPixmap(pixmap)
        grid.addWidget(self.label1)
        grid.addWidget(self.label2)
        self.setLayout(grid)