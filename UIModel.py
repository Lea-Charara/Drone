class Model:
    def __init__( self ):
        self.fileName = None
        self.fileContent = ""

    def isValid( self ):
        try:
            with open( self.fileName, 'rb') as f:
                tkoff = f.readline().decode().split()[0]
                f.seek(-3, 2)
                end = f.readline().decode()
                f.close()
            if tkoff == "takeoff" and end == "end":
                return True
            return False
        except:
            return False
            
    def getFileName( self ):
        return self.fileName
        
    def setFileName( self, fileName ):
        self.fileName = fileName     
