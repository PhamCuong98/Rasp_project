import mysql.connector
"""
host= "123.19.252.125"
user= "root"
password= "Ngoccuong@1812"
database= "mydatabase"""

host= "localhost"
user= "root"
password= "ngoccuong1812"
database= "mydatabase"

class IN_SQL(object):
    def __init__(self, infor, data):
        self.infor= infor
        self.data= data
    def public_realtime(self):
        self.mydb= mysql.connector.connect(host=host, user=user, password=password, database= database)
        self.mycursor= self.mydb.cursor()
        sql= "INSERT INTO realtime (time, day, number, ID) VALUES (%s, %s, %s, %s)"
        self.mycursor.execute(sql, self.infor)
        self.mydb.commit()
        print(self.mycursor.rowcount, "Da Insert")

    def public_data(self):
        self.mydb= mysql.connector.connect(host=host, user=user, password=password, database= database)
        self.mycursor= self.mydb.cursor()
        sql= "INSERT INTO data (time, day, number, status, ID) VALUES (%s, %s, %s, %s, %s)"
        self.mycursor.execute(sql, self.data)
        self.mydb.commit()
        print(self.mycursor.rowcount, "Da Insert")

class OUT_SQL(object):
    def __init__(self, infor, data):
        self.infor= infor
        self.data= data
    def Search(self):
        self.mydb= mysql.connector.connect(host=host, user=user, password=password, database= database)
        self.mycursor= self.mydb.cursor()
        myresult= []
        licenses= self.infor[0]
        RFID= self.infor[1]
        print(licenses)
        sql_search = "SELECT * FROM realtime WHERE ID = '" + str(RFID)+ "'"
        self.mycursor.execute(sql_search)
        myresult = self.mycursor.fetchall()
        print(myresult)
        print(myresult[0][2])

        if myresult == []:
            print("ko tim thay")
            notice= "The RFID chua gan infor"
            return notice

        elif licenses != myresult[0][2]:
            print("khong tim thay")
            notice= "Sai Xe - Kiem tra lai"
            return notice
        else:
            sql_delete = "DELETE FROM realtime WHERE number = '" + str(licenses)+ "'"
            self.mycursor.execute(sql_delete)
            self.mydb.commit()
            print(self.mycursor.rowcount, "Da Delete")
            notice= "Da Xoa"
            return notice
    
    def public_data(self):
        self.mydb= mysql.connector.connect(host=host, user=user, password=password, database= database)
        self.mycursor= self.mydb.cursor()
        sql= "INSERT INTO data (time, day, number, status, ID) VALUES (%s, %s, %s, %s, %s)"
        self.mycursor.execute(sql, self.data)
        self.mydb.commit()
        print(self.mycursor.rowcount, "Da Insert")


if __name__ == '__main__':
    main()