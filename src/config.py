from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QHBoxLayout, QDialog ,QApplication,QPushButton,QWidget, QMainWindow, 
QMessageBox, QLineEdit,QTabWidget, QLabel, QAction, QVBoxLayout, QGroupBox, QFileDialog)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread

import sys
import cv2
import numpy as np
import os
import time
from datetime import datetime
import argparse
from PIL import Image, ImageFont, ImageDraw
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


YOLO_CONFIG = r"Source_rasp/src/yolo/yolov4-tiny-custom.cfg"
YOLO_WEIGHT = r"Source_rasp/src/yolo/yolov4-tiny-custom_last.weights"
YOLO_CLASSES = r"Source_rasp/src/yolo/obj.names"

MODEL = r"Model/my_model.h5"

LABEL_DATA = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C','D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z', 'None']

WIN_TOP = 10
WIN_LEFT = 10
WIN_HEIGHT = 720
WIN_WIDTH = 1280

SIZE_CAM_WIDTH = 600
SIZE_CAM_HEIGHT = 700

WIDTH_IMG = 800
HEIGHT_IMG = 600
SIZE_IMAGE = (WIDTH_IMG, HEIGHT_IMG)

WIDTH_YOLO = 300
HEIGHT_YOLO = 200
SIZE_YOLO = (WIDTH_YOLO, HEIGHT_YOLO)

PORT_USB = "/dev/ttyUSB0"
