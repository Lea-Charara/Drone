from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(332, 213)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.WlcmLbl = QtWidgets.QLabel(self.centralwidget)
        self.WlcmLbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.WlcmLbl.setAutoFillBackground(False)
        self.WlcmLbl.setTextFormat(QtCore.Qt.RichText)
        self.WlcmLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.WlcmLbl.setObjectName("WlcmLbl")        
        self.verticalLayout.addWidget(self.WlcmLbl)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.NewBttn = QtWidgets.QPushButton(self.centralwidget)
        self.NewBttn.setObjectName("NewBttn")
        self.horizontalLayout.addWidget(self.NewBttn)
        
        self.OpenBttn = QtWidgets.QPushButton(self.centralwidget)
        self.OpenBttn.setObjectName("OpenBttn")
        self.horizontalLayout.addWidget(self.OpenBttn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(50)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.PathLbl = QtWidgets.QLabel(self.centralwidget)
        self.PathLbl.setText("")
        self.PathLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.PathLbl.setObjectName("PathLbl")
        self.horizontalLayout_2.addWidget(self.PathLbl)
        
        self.StrtBttn = QtWidgets.QPushButton(self.centralwidget)
        self.StrtBttn.setEnabled(False)
        self.StrtBttn.setObjectName("StrtBttn")
        self.horizontalLayout_2.addWidget(self.StrtBttn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 332, 26))
        self.menubar.setObjectName("menubar")
        self.menuDrone_App = QtWidgets.QMenu(self.menubar)
        self.menuDrone_App.setObjectName("menuDrone_App")
        MainWindow.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setShortcut("")
        self.actionExit.setObjectName("actionExit")
        self.menuDrone_App.addAction(self.actionNew)
        self.menuDrone_App.addAction(self.actionOpen)
        self.menuDrone_App.addAction(self.actionExit)
        self.menubar.addAction(self.menuDrone_App.menuAction())

        self.retranslateUi(MainWindow)
        self.OpenBttn.clicked.connect(self.browseSlot)
        self.NewBttn.clicked.connect(self.newSlot)
        self.actionNew.triggered.connect(self.newSlot)
        self.actionOpen.triggered.connect(self.browseSlot)
        self.actionExit.triggered.connect(MainWindow.close)
        self.StrtBttn.clicked.connect(self.startSlot)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Parking Detector"))
        self.WlcmLbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Welcome!</span></p></body></html>"))
        self.NewBttn.setText(_translate("MainWindow", "New Path"))
        self.OpenBttn.setText(_translate("MainWindow", "Load a Path"))
        self.StrtBttn.setText(_translate("MainWindow", "Start"))
        self.menuDrone_App.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    @pyqtSlot()
    def browseSlot(self):
        pass
        
    @pyqtSlot()
    def newSlot(self):
        pass 
        
    @pyqtSlot()
    def startSlot(self):
        pass        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
