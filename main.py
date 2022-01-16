import sys
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)
from imageviewer import ImageViewer, ImageViewer2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Camera Calibration OpenCV")
        self.initUI()
        self.prepare_data()
    
    def initUI(self):
        button = [None] * 5
        button[0] = QPushButton("1. Find Corners", self)
        button[0].clicked.connect(self.find_corners)
        button[1] = QPushButton("2. Find Intrinsic", self)
        button[1].clicked.connect(self.find_intrinsic)
        button[2] = QPushButton("3. Find Extrinsic", self)
        button[2].clicked.connect(self.find_extrinsic)
        button[3] = QPushButton("4. Find Distortion", self)
        button[3].clicked.connect(self.find_distortion)
        button[4] = QPushButton("5. Show Undistort Images", self)
        button[4].clicked.connect(self.show_undistorted)
        self.select_textbox = QLineEdit("1")

        vbox = QVBoxLayout()
        vbox.addWidget(button[0])
        vbox.addWidget(button[1])
        vbox.addWidget(QLabel("Select image:"))
        vbox.addWidget(self.select_textbox)
        vbox.addWidget(button[2])
        vbox.addWidget(button[3])
        vbox.addWidget(button[4])
        vbox.addStretch(1)
        self.setLayout(vbox)
    
    def prepare_data(self):
        """
        Take reference from https://opencv24-python-tutorials.readthedocs.io/en/latest/
        py_tutorials/py_calib3d/py_calibration/py_calibration.html
        """

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0), ..., (7,10,0)
        x, y = 9, 6
        objp = np.zeros((x * y, 3), np.float32)
        objp[:,:2] = np.mgrid[0:x, 0:y].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        paths = [f"chessboard/{i}.jpg" for i in range(1, 14)]
        self.orig_imgs = []
        self.corner_imgs = []
        for path in paths:
            img = cv2.imread(path)
            self.orig_imgs.append(cv2.imread(path))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (x, y), None)
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (x, y), (-1,-1), criteria)
            imgpoints.append(corners2)
            img = cv2.drawChessboardCorners(img, (x, y), corners2, ret)
            self.corner_imgs.append(img)
        
        ret, self.mtx, self.dist, self.rvecs, self.tvecs = \
        cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


    def find_corners(self):
        self.imgviewer = ImageViewer(self.corner_imgs)
        self.imgviewer.show()

    def find_intrinsic(self):
        print("Intrinsic:")
        print(self.mtx)

    def find_extrinsic(self):
        img_id = int(self.select_textbox.text()) - 1
        R, _ = cv2.Rodrigues(self.rvecs[img_id])
        RT = np.concatenate((R, self.tvecs[img_id]), axis=1)
        print("Extrinsic:")
        print(RT)

    def find_distortion(self):
        print("Distortion:")
        print(self.dist)

    def show_undistorted(self):
        img_id = int(self.select_textbox.text()) - 1
        img1 = self.orig_imgs[img_id].copy()
        h, w = img1.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
        
        # undistort
        dst = cv2.undistort(img1, self.mtx, self.dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite('tmp.png', dst)
        img2 = cv2.imread('tmp.png')
        self.imgviewer = ImageViewer2(self.orig_imgs[img_id], img2)
        self.imgviewer.show()

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()