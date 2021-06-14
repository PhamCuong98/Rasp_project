from src.config import *
from func_process import yolotiny
from process_MySQL import IN_SQL, OUT_SQL
import serial

class processCamera(QWidget):
    def __init__(self, npImage, note):
        super().__init__()
        #Input: array of image read from cv2.
        self.np_Image= npImage
        self.note= note
        self.show()

    def convert_data(self, np_Image):
        self.setGeometry( 300, 300, 350, 300 )
        self.setWindowTitle( 'Review' )
        self.show()

        #class of Func_process.py. 
        image = cv2.resize(np_Image, SIZE_IMAGE)
        process= yolotiny(image)
        licenses, result_arr = process.cut_plate()
        """print(licenses)
        print(result_arr.shape)"""

        # Show image capture, what was choose to process
        self.horizontalLayout = QHBoxLayout()
        qimage1 = QImage(np_Image, np_Image.shape[1], np_Image.shape[0], QImage.Format_RGB888)   
        pic = QPixmap(qimage1)
        label= QLabel()
        label.setPixmap(pic)
        label.resize(WIDTH_YOLO, HEIGHT_YOLO)
        self.horizontalLayout.addWidget(label)

        # Show plate after process
        result_arr_3=np.stack((result_arr,)*3, -1)
        qimage2 = QImage(result_arr_3, result_arr_3.shape[1], result_arr_3.shape[0], QImage.Format_RGB888)                                                                                                                                                         
        yolo = QPixmap(qimage2)
        label_yolo = QLabel()
        label_yolo.setPixmap(yolo)
        label_yolo.resize(WIDTH_YOLO, HEIGHT_YOLO)
        self.horizontalLayout.addWidget(label_yolo)

        # Button to select choose
        self.horizontalLayout2 = QHBoxLayout()
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(lambda:self.exit())
        send = QPushButton('IN')
        if self.note == "IN":
            send.clicked.connect(lambda:self.sendINMySQL(licenses))
        else:
            send.clicked.connect(lambda:self.sendOUTMySQL(licenses))
        self.horizontalLayout2.addWidget(cancel)
        self.horizontalLayout2.addWidget(send)

        # Label to show result: Output
        self.verticalLayout = QVBoxLayout()
        text1= QLabel("Ket qua")
        text1.move(200,200)
        text2= QLabel(licenses)
        text2.move(250,200)
        self.verticalLayout.addWidget(text1)
        self.verticalLayout.addWidget(text2)
        
        # Connect widget to GUI
        self.verticalEnd = QVBoxLayout(self)
        self.verticalEnd.addLayout(self.horizontalLayout)
        self.verticalEnd.addLayout(self.horizontalLayout2)
        self.verticalEnd.addLayout(self.verticalLayout)
        self.setLayout(self.verticalEnd)

    # Func exit-connect with button Cancel
    def exit(self):
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            self.close()
        else:
            pass

    
    # Func send infor - connect with button "IN"
    def sendINMySQL(self, licenses):
        infor_realtime= []  
        infor_data= []
        time, day= self.getTime()
        ser = serial.Serial(PORT_USB, 9600, rtscts=True,dsrdtr=True)
        print(ser.name)         # check which port was really used
        ID=""
        ID = ser.readline().decode('UTF-8')
        ser.close()
        print("RFID: "+ str(ID))
        infor_realtime.append(time)
        infor_realtime.append(day)
        infor_realtime.append(licenses)
        infor_realtime.append(ID)

        infor_data.append(time)
        infor_data.append(day)
        infor_data.append(licenses)
        infor_data.append("IN")
        infor_data.append(ID)

        sql= IN_SQL(infor_realtime, infor_data)
        sql.public_realtime()
        sql.public_data()
        message= str(licenses)+" - "+str(ID)
        self.NoteMysql(message)
        self.close()
        #self.exit()

    # Func send infor - connect with button "OUT"
    def sendOUTMySQL(self, licenses):
        infor_real=[]
        infor_data= []
        notice=[]
        time, day= self.getTime()
        ser = serial.Serial(PORT_USB, 9600, rtscts=True, dsrdtr=True)
        print(ser.name)         # check which port was really used
        ID=""
        ID = ser.readline().decode('UTF-8')
        ser.close()
        print("RFID: "+ str(ID))
        infor_real.append(licenses)
        infor_real.append(ID)

        infor_data.append(time)
        infor_data.append(day)
        infor_data.append(licenses)
        infor_data.append("OUT")
        infor_data.append(ID)

        sql= OUT_SQL(infor_real, infor_data)
        notice= sql.Search()
        message= str(licenses) +"-"+str(licenses)+" - "+notice
        self.NoteMysql(message)
        sql.public_data()
        self.close()
        #self.exit()    
    # Message show information of mysql    
    def NoteMysql(self, message):
        #print("xuat note mysql")
        QMessageBox.about(self, "Thong bao tu Mysql", message)

    def getTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_day = now.strftime("%d/%m/%Y")
        return current_time, current_day

class processImage(QWidget):
    def __init__(self, path_img):
        super().__init__()
        self.path_img= path_img
        self.initUI()
    
    def initUI(self):
        self.show()

    def getImage(self, path_img):
        #self.setGeometry( 300, 300, 350, 300 )
        self.setWindowTitle('Xu ly image')
        self.show()
        
        image= cv2.imread(path_img)
        image = cv2.resize(image, SIZE_IMAGE)
        process= yolotiny(image)
        licenses, result_arr = process.cut_plate()
        print(licenses)
        """#licenses.reverse()
        print("ádsa")
        print(result_arr.shape)"""

        self.horizontalLayout = QHBoxLayout()
        pic = QPixmap(path_img)
        label= QLabel()
        label.setPixmap(pic)
        label.resize(WIDTH_YOLO, HEIGHT_YOLO)
        self.horizontalLayout.addWidget(label)

        result_arr_3=np.stack((result_arr,)*3, -1)
        qimage = QImage(result_arr_3, result_arr_3.shape[1], result_arr_3.shape[0],QImage.Format_RGB888)                                                                                                                                                               
        yolo = QPixmap(qimage)
        label_yolo = QLabel()
        label_yolo.setPixmap(yolo)
        label_yolo.resize(WIDTH_YOLO, HEIGHT_YOLO)
        self.horizontalLayout.addWidget(label_yolo)

        self.horizontalLayout2 = QHBoxLayout()
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(lambda:self.exit())
        sendIN = QPushButton('IN')
        sendIN.clicked.connect(lambda:self.sendINMySQL(licenses))
        sendOUT = QPushButton('OUT')
        sendOUT.clicked.connect(lambda:self.sendOUTMySQL(licenses))
        self.horizontalLayout2.addWidget(cancel)
        self.horizontalLayout2.addWidget(sendIN)
        self.horizontalLayout2.addWidget(sendOUT)

        self.verticalLayout = QVBoxLayout()
        text1= QLabel("Ket qua")
        text1.move(200,200)
        text2= QLabel(licenses)
        text2.move(250,200)
        self.verticalLayout.addWidget(text1)
        self.verticalLayout.addWidget(text2)

        self.verticalEnd = QVBoxLayout(self)
        self.verticalEnd.addLayout(self.horizontalLayout)
        self.verticalEnd.addLayout(self.horizontalLayout2)
        self.verticalEnd.addLayout(self.verticalLayout)
        self.setLayout(self.verticalEnd)

    def exit(self):
        print("PhamCuong_1st")
        reply = QMessageBox.question(
            self, "Message",
            "Bạn muốn thoát?.",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            self.close()
        else:
            pass
    
    def NoteMysql(self, message):
        print("xuat note mysql")
        QMessageBox.about(self, "Thong bao tu Mysql", message)
        
    def sendINMySQL(self, licenses):
        ser = serial.Serial(PORT_USB, 9600, rtscts=True, dsrdtr=True)
        print(ser.name)         # check which port was really used
        ID=""
        ID = ser.readline().decode('UTF-8')
        ser.close()
        print("RFID: "+ str(ID))
        infor_realtime= []
        infor_data= []
        time, day= self.getTime()

        infor_realtime.append(time)
        infor_realtime.append(day)
        infor_realtime.append(licenses)
        infor_realtime.append(ID)

        infor_data.append(time)
        infor_data.append(day)
        infor_data.append(licenses)
        infor_data.append("IN")
        infor_data.append(ID)

        sql= IN_SQL(infor_realtime, infor_data)
        sql.public_realtime()
        sql.public_data()
        message= str(licenses)+" - "+str(ID)
        self.NoteMysql(message)
        self.close()
        #self.exit()
    
    def sendOUTMySQL(self, licenses):
        infor_real=[]
        infor_data= []
        notice=[]
        time, day= self.getTime()
        ser = serial.Serial(PORT_USB, 9600, rtscts=True, dsrdtr=True)
        print(ser.name)         # check which port was really used
        ID=""
        ID = ser.readline().decode('UTF-8')
        ser.close()
        print("RFID: "+ str(ID))
        infor_real.append(licenses)
        infor_real.append(ID)

        infor_data.append(time)
        infor_data.append(day)
        infor_data.append(licenses)
        infor_data.append("OUT")
        infor_data.append(ID)

        sql= OUT_SQL(infor_real, infor_data)
        notice= sql.Search()
        message= str(licenses) +"-"+str(licenses)+" - "+notice
        self.NoteMysql(message)
        sql.public_data()
        self.close()
        #self.exit()
        
    def getTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_day = now.strftime("%d/%m/%Y")
        return current_time, current_day

if __name__ == '__main__':
    main()