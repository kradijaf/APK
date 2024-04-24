from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

class Draw(QWidget):
    '''
    - Class for program´s graphical operations.

    - Methods:
        - __init__(*args, **kwargs) - the constructor with default parameters necessary for Qt, sets up the framework for drawing on the widget
        - mousePressEvent(e: QMouseEvent) - Reacts to mouse click on widget resulting in drawing the tested point / a point to the polygon
        - paintEvent(e: QPaintEvent) - Refreshes the widget
        - messageBox(title: str, text : str) -  Creates a message box with given text
        - clearData() - Sets drawing framework data to default values
        - clearMBRs() - Removes minimum bounding rectangles
        - getter type functions -> Obtain class´ data for usage in other classes of the programme
        - setter type functions -> Set attribute to data from results of other classes of the programme
    '''

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.q = QPointF(10, 10)                    # initial point
        self.bld = QPolygonF()                      # initial building
        self.blds = {1 : self.bld}                  # all the buildings in the framework
        self.mbrs = dict()                          # minimum bounding rectangles

    def mousePressEvent(self, e : QMouseEvent) -> None:
        if len(self.blds) > 1:
            self.messageBox('Operation unavailable', 'Can´t modify polygon when multiple polygons exist.')
        else:
            self.bld.append(QPointF(e.position().x(), e.position().y()  ))      # Convert cursors coordinates to Q Point F data type and add itto the polygon
            self.mbrs = dict()                                                  # Remove current mbr because It would not be related to an edited building

        self.repaint()                              # Sync the canvas  

    def paintEvent(self, e : QPaintEvent) -> None:          # The method called by self.repaint() 
        qp = QPainter(self)                                 # Create the painter

        qp.setPen(Qt.GlobalColor.black)                     # polygon will be drawn in yellow color
        qp.setBrush(Qt.GlobalColor.yellow)
        for bld in self.blds.values():
            qp.drawPolygon(bld)                             # Draw each polygon

        qp.setPen(Qt.GlobalColor.red)                       # MBR will be drawn using transparent outline
        qp.setBrush(Qt.GlobalColor.transparent)
        for mbr in self.mbrs.values():                      # Draw each MBR
            qp.drawPolygon(mbr) 

        qp.end()                                            # Delete painter object 

    def messageBox(self, title: str, text : str) -> None:           
        mb = QMessageBox()
        mb.setWindowTitle(title)
        mb.setText(text)
        mb.exec()                                           # Show the message box

    def clearData(self) -> None:
        self.q = QPointF(10, 10)

        self.bld = QPolygonF()          # clear 1st building
        self.blds = {1 : self.bld}      # clear buildings
        self.mbrs = dict()              # clear MBRs

        self.repaint()       

    def clearMBRs(self) -> None:
        self.mbrs = dict()
        self.repaint()      
        
    def getBlds(self) -> dict:
        return self.blds                
    
    def getMBRs(self) -> dict:
        return self.mbrs                

    def getWidth(self) -> int:
        return self.width()
    
    def getHeight(self) -> int:
        return self.height()
    
    def setBlds(self, blds : dict) -> None:
        self.blds = blds
        self.bld = self.blds[1]                     
        self.repaint()  

    def setMBRs(self, mbrs) -> None:
        self.mbrs = mbrs