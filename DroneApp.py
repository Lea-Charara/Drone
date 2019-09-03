from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from DroneAppUI import Ui_MainWindow
import sys
from UIModel import Model

import DroneProject as drone

class MainWindowUIClass( Ui_MainWindow ):
    def __init__( self ):
        '''Initialize the super class
        '''
        super().__init__()
        self.model = Model()
        self.filePath = None
        self.Mode = 0
        self.MW = None
        ''' 
        If mode = -1, Read
        If mode = 1, Write
        '''
        
    def setupUi( self, MW ):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi( MW )
        self.MW = MW

    def refresh( self ):
        self.filePath = self.model.getFileName()
        self.PathLbl.setText( self.filePath )
        self.StrtBttn.setEnabled(True)
        
    def clear( self ):
        self.filePath = None
        self.PathLbl.setText( "" )
        self.StrtBttn.setEnabled(False)
        
    
    # Error Message Box
    def showdialog( self ):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setText("Please select a valid drone file.")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)    
        msg.exec_()
        self.clear()
        
    # slot
    def newSlot( self ):
        ''' Called when the user presses the New button
        '''
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "New File", "", "Text (*.txt)");
        self.model.setFileName( fileName )
        self.refresh()
        self.Mode = 1
        
    # slot
    def browseSlot( self ):
        ''' Called when the user presses the Open button
        '''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "Select a valid file.",
                        "",
                        "Text Files (*.txt)",
                        options=options)
        if fileName:
            self.model.setFileName( fileName )
            if self.model.isValid():
                self.Mode = -1
                self.refresh()
                return
        self.showdialog()
            
    # slot
    def startSlot( self ):
        if self.Mode < 0:
            drone.ReadPath(self.filePath)
        elif self.Mode > 0:
            drone.WritePath(self.filePath)
        
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()

if __name__ == '__main__': main()