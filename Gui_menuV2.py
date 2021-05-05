from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QHBoxLayout, QDialog ,QApplication,QPushButton,QWidget, QMainWindow, 
QMessageBox, QLineEdit,QTabWidget, QLabel, QAction, QVBoxLayout, QGroupBox, QFileDialog, QGridLayout)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from Gui_processV2 import processCamera, processImage
import sys
import cv2
import numpy as np

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self): 
        super().__init__()
        self._run_flag = True

    def run(self):

        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title= "Detect license plate"      
        self.left= 10
        self.top= 10
        self.height= 720
        self.width= 1280
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        mainMenu = self.menuBar()
        exit_UI= mainMenu.addMenu('Exit')
        self.exit_Button(exit_UI)
        
        self.table_widget= UIWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    def exit_Button(self, UI):
        exit_Button= QAction('Exit', self)
        exit_Button.setShortcut('Ctrl+Q')
        exit_Button.setStatusTip('Exit.application')
        exit_Button.triggered.connect(self.close)
        UI.addAction(exit_Button)
    
class UIWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.disply_width = 600
        self.display_height = 700
        layout= QHBoxLayout(self)
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()   
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        # Add tabs
        self.tabs.addTab(self.tab1,"Camera")
        self.tabs.addTab(self.tab2,"Image")

        """------------------- TAB 1 ---------------------------"""
        """----------------------IN------------"""
        self.Camera_IN = QtWidgets.QGroupBox("Camera IN")
        self.layout_IN = QtWidgets.QGridLayout() 
        self.displayIN = QLabel(self)
        
        self.layout_IN.addWidget(self.displayIN, 0,0,1,2,alignment=QtCore.Qt.AlignCenter)
        self.chooseIN= QPushButton('Camera IN')
        self.chooseIN.clicked.connect(self.openCamera_IN)
        self.layout_IN.addWidget(self.chooseIN,1,0)

        self.DetectIN= QPushButton('DETECT IN')
        self.DetectIN.clicked.connect(self.choose_img_IN)
        self.layout_IN.addWidget(self.DetectIN,1,1) 

        self.Camera_IN.setLayout(self.layout_IN)

        """--------------------OUT----------"""
        self.Camera_OUT = QtWidgets.QGroupBox("Camera OUT")
        self.layout_OUT = QtWidgets.QGridLayout()

        self.displayOUT = QLabel(self)
        self.layout_OUT.addWidget(self.displayOUT, 0,0,1,2,alignment=QtCore.Qt.AlignCenter)

        self.chooseOUT= QPushButton('Camera OUT')
        self.chooseOUT.clicked.connect(self.openCamera_OUT)
        self.layout_OUT.addWidget(self.chooseOUT,1,0)

        self.DetectOUT= QPushButton('DETECT OUT')
        self.DetectOUT.clicked.connect(self.choose_img_OUT)
        self.layout_OUT.addWidget(self.DetectOUT,1,1) 

        self.Camera_OUT.setLayout(self.layout_OUT)

        """-------------------UI camera-------------"""
        self.cameraGroupBox= QGroupBox("Control")
        self.layout = QtWidgets.QGridLayout() 
        self.layout.addWidget(self.Camera_IN,0,0)

        self.layout.addWidget(self.Camera_OUT,0,1)
        self.cameraGroupBox.setLayout(self.layout)

        """-----------------Add grouBox to tab 1------------"""
        self.tab1.layout= QHBoxLayout(self)
        self.tab1.layout.addWidget(self.cameraGroupBox)
        self.tab1.setLayout(self.tab1.layout)

        """-------------------------- TAB 2---------------------------"""
        self.tab2.layout= QVBoxLayout(self)
        #Tạo các extension cho tab 2
        self.pushbutton1Tab2= QPushButton("Them path Image")
        self.pushbutton1Tab2.clicked.connect(self.openImage)
        
        self.tab2.layout.addWidget(self.pushbutton1Tab2)

        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def openCamera_IN(self):
        print("1st")
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image_IN)
        # start the thread
        self.thread.start()
        self.chooseIN.setEnabled(False)
        self.chooseOUT.setEnabled(False)
        self.DetectOUT.setEnabled(False)

    def choose_img_IN(self):
        #self.click()
        note= "IN"
        self.thread.change_pixmap_signal.connect(self.get_img_IN)
        self.thread.stop()
        self.chooseIN.setEnabled(True)
        self.chooseOUT.setEnabled(True)
        self.DetectOUT.setEnabled(True)

    def openCamera_OUT(self):
        print("1st")
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image_OUT)
        # start the thread
        self.thread.start()
        self.chooseIN.setEnabled(False)
        self.chooseOUT.setEnabled(False)
        self.DetectIN.setEnabled(False)

    def choose_img_OUT(self):
        #self.click()
        self.thread.change_pixmap_signal.connect(self.get_img_OUT)
        self.thread.stop()
        self.chooseIN.setEnabled(True)
        self.chooseOUT.setEnabled(True)
        self.DetectIN.setEnabled(True)
    
    def get_img_IN(self, cv_img):
        #print(type(cv_img))
        note= "IN"
        self.process= processCamera(cv_img, note)
        self.process.convert_data(cv_img)
    
    def get_img_OUT(self, cv_img):
        #print(type(cv_img))
        note="OUT"
        self.process= processCamera(cv_img, note)
        self.process.convert_data(cv_img)
    
    #<----------------------------Func for tab 2--------------------------->
    def openImage(self):
        path_img= self.openFileNameDialog()
        print(path_img)
        self.process= processImage(path_img)
        self.process.getImage(path_img)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        """if fileName:
            print(type(fileName))"""
        return fileName
        

    @pyqtSlot(np.ndarray)
    def update_image_IN(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.displayIN.setPixmap(qt_img)

    def update_image_OUT(self, cv_img):
        #Updates the image_label with a new opencv image
        qt_img = self.convert_cv_qt(cv_img)
        self.displayOUT.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p) 

def main():
    app= QApplication(sys.argv)
    ex= App()
    ex.show()
    sys.exit(app.exec_())
 
if __name__== '__main__':
    main()