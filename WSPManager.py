



from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import QMessageBox
import subprocess as sp
import datetime
import re
import webbrowser
import threading 

class Ui_MainWindow(object):
    def About(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText("Wifi Saved Password 1.0\nSimple Utility Tool To See Saved Wifi Passwords.\nEmail:rmcservices20@gmail.com")
        msg.setStandardButtons(QMessageBox.Yes)
        msg.setWindowTitle("About")
        replay=msg.exec_()
         
    #Show Version Number  
    def Version(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText("Wifi Saved Password \nVersion:1.0")
        msg.setStandardButtons(QMessageBox.Yes)
        msg.setWindowTitle("About")
        replay=msg.exec_()
        
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(509, 379)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/About.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")
        
        self.actionVersion = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/Version.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVersion.setIcon(icon2)
        self.actionVersion.setObjectName("actionVersion")
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/RefreshI.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon4)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon5)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionRefresh)
        self.GetWifiNames()

        #All Menu Clicked Event
        self.actionAbout.triggered.connect(self.About)
        self.actionVersion.triggered.connect(self.Version)
        self.actionSave.triggered.connect(self.Save)

        #Handle Toolbar event
        self.actionRefresh.triggered.connect(self.StartReScanning)

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def Save(self):
        mytable=self.tableWidget.rowCount()
        paths=os.path.expanduser('~')
        outputfile=os.path.join(paths,"WifiPasswords")
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
        out_file=open(os.path.join(outputfile,"Passwords.txt"),"w+")
        out_file.write('{0:*^60s}'.format("*"))
        out_file.write('\nThis Is Autogenerated File Contains Saved Wifi Passwords \nAuthor:Ravishankar Chavare\nVersion:1.0\nDateTime:{}'.format(str(datetime.datetime.now())))
        out_file.write('\n\n{0:*^60s}'.format("*"))
        for i in range(0,mytable):
            srno=self.tableWidget.item(i,0)
            wifi=self.tableWidget.item(i,1)
            password=self.tableWidget.item(i,2)
            out_file.write('\n{0:-^35s}'.format(" WIFI "+srno.text()))
            out_file.write("\nName:{}\nPassword:{}\n".format(str(wifi.text()),str(password.text())))
        out_file.close()
        path=os.path.realpath(outputfile)
        os.startfile(path)
        
                

       

    def StartReScanning(self):
        self.tableWidget.setRowCount(0)
        self.GetWifiNames()
        
    def GetWifiNames(self):
        ssidnames= sp.getstatusoutput("netsh wlan show profiles")
        ssd=ssidnames[1].split("All User Profile     :")
        for s in ssd[1:]:
            t1=threading.Thread(target=self.GetPassword,args=(s.strip(),))
            t1.start()

    def SetWifiToList(self,i,wifi,password):
        #self.tableWidget.setRowCount(0)
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)
        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(numRows+1)))

        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(wifi))
        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(password))
        
    def GetPassword(self,wifi):
        status,passtext=sp.getstatusoutput('netsh wlan show profile "{}" key=clear'.format(wifi))
        if status==0:
                #print(passtext)
                passs=re.findall(r"Key Content            : [\w.-]+",passtext)
                if(len(passs)!=0):
                    password=passs[0].split(":")[1]
                    self.SetWifiToList(1,wifi,password)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wifi Password Viewer"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Sr. No"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Wifi Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Password"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionRefresh.setToolTip(_translate("MainWindow", "Refresh"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

