import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from SpotsUI import Ui_Dialog
from PyQt5.QtWidgets import QDialog

class SpotsClass (Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.Parked = -1
        self.Spots = -1
        self.MW = None
        
    def setupUi( self, MW ):
        self.MW = MW
        super().setupUi( MW )

    def clear( self ):
        self.spotsTxt.clear()
        
    def close( self ):
        self.MW.close()
        self.clear()
        
    def setParked( self, parked ):
        self.Parked = int( parked )

    def showdialog( self, id):
        msg = QtWidgets.QMessageBox()
        
        if id == -1:
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Please input a valid number.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            
        elif id == 1:
            res = self.Spots - self.Parked
            if not res < 0:
                msg.setIcon(QtWidgets.QMessageBox.Information)            
                msg.setText("You have %s space(s) available." % ( res ,) )
                msg.setWindowTitle("Result")
            else:
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("%s vehicule(s) have been detected but your parking can only fit %s vehicule(s)!\r\nPlease make sure that the area is empty and that you gave a correct number of spaces." % ( self.Parked , self.Spots ))
                msg.setWindowTitle("Error")
                
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            
        msg.exec_()

    
    def spotsSlot( self ):    
        try:
            self.Spots = int(self.spotsTxt.text().strip())
        except:
            self.showdialog(-1)  
            self.clear()
            return
        self.close() 
    def getparked ():
        return ui.Parked
            

app = QtWidgets.QApplication(sys.argv)
DialogWindow = QtWidgets.QDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
ui = SpotsClass()
ui.setupUi(DialogWindow)

# Shows how many spots are available by doing (how many spots) - (res)

def resDialog(res):
    ui.setParked(res)
    ui.showdialog(1)
    return

# Shows the user the window where he can input how many spots he has

def show():
    DialogWindow.exec_()
    return

