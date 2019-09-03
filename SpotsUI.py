from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot

class Ui_Dialog( object ):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 115)
        Dialog.setMaximumSize(QtCore.QSize(453, 115))
        Dialog.setWindowTitle("Parking Detector")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        
        Dialog.setWhatsThis("")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        
        self.label.setFont(font)
        self.label.setText("Please input how many parking spots you have.")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        
        self.spotsTxt = QtWidgets.QLineEdit(Dialog)
        self.spotsTxt.setObjectName("spotsTxt")
        self.gridLayout.addWidget(self.spotsTxt, 1, 0, 1, 1)
        
        self.okBttn = QtWidgets.QPushButton(Dialog)
        self.okBttn.setObjectName("okBttn")
        self.gridLayout.addWidget(self.okBttn, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.okBttn.clicked.connect(self.spotsSlot)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.spotsTxt, self.okBttn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.okBttn.setText(_translate("Dialog", "OK"))

    @pyqtSlot()
    def spotsSlot(self):
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
