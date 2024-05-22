from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):
    '''
    - Class for program´s main window and connecting operations in other classes.

    - Methods:
        - __init__(*args, **kwargs) - the constructor with default parameters necessary for Qt, sets up the framework for drawing on the widget
        - mousePressEvent(e: QMouseEvent) - Reacts to mouse click on widget resulting in drawing the tested point / a point to the polygon
        - setPolygons(polygons : dict) - Refreshes polygon database on input 
        - setHighlighted(highlighted : dict = {}) - Refreshes the dict of keys of polygons to highlight, Also used for clearing the list via the default value
        - paintEvent(e: QPaintEvent) - Refreshes the widget
        - switchDrawing() - Switches between drawing the tested point and adding a point to the polygon
        - messageBox(title: str, text : str) -  Creates a message box with given text
        - clearData() - Sets drawing framework data to default values
        - getter type functions -> Draw items
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.q = QPointF(10, 10)                # the tested point
        self.pol = [[], QPolygonF(), ()]        # The selected polygon: [real coordinates, Qt polygon data type, widget coordinates bounding box]      
        self.polygons = {1 : self.pol}          # All polygons in the framework
        self.highlighted = {}                   # polygons to highlight (point inside polygon / on its edge / is its vertex)

        self.add_vertex = True                  # decides whether to draw the tested point / add a point to the polygon

    def mousePressEvent(self, e: QMouseEvent):
        x = e.position().x()
        y = e.position().y()                    # Get point coordinates

        if self.getAddV():                      # Append point to polygon
            p = QPointF(x, y)                  
            self.pol[1].append(p)      
            self.pol[0] = []                    # Delete real coordinates because the number of real and pixel coordinates can't match anymore
            self.highlighted.clear()            # Clear the dict of keys of polygons to highlight - the edited polygon could have been highlighted
        else:
            self.q.setX(x); self.q.setY(y)      # Shift tested point

        self.repaint()                          # Sync the canvas

    def setPolygons(self, polygons : dict):
        self.polygons = polygons
        self.pol = self.polygons[1]             # sync polygon data         

        if len(self.polygons) > 1:              # Disable editing polygons if more than one polygon exist, user can't choose which one to edit   
            self.add_vertex = False

        self.repaint()    

    def setHighlighted(self, highlighted : dict = {}):
        self.highlighted = highlighted

    def paintEvent(self, e: QPaintEvent):       # The method called by self.repaint() 
        qp = QPainter(self)                     # Create the painter

        qp.setPen(Qt.GlobalColor.red)           # set polygon color to yellow with red outline
        qp.setBrush(Qt.GlobalColor.yellow)   
        for pol in self.polygons.values():      # Draw each negatively tested polygon
            qp.drawPolygon(pol[1])

        qp.setPen(Qt.GlobalColor.red)           # set polygon color to blue 
        qp.setBrush(Qt.GlobalColor.blue)
        for pol in self.highlighted.values():   # Draw each positively tested polygon
            qp.drawPolygon(pol[1])

        r = 6                                   # Point´s diameter
        qp.setPen(Qt.GlobalColor.green)       
        qp.setBrush(Qt.GlobalColor.green)
        qp.drawEllipse(int(self.q.x() - r), int(self.q.y() - r), 2 * r, 2 * r)

        r = 2      
        qp.setPen(Qt.GlobalColor.darkBlue)       
        qp.setBrush(Qt.GlobalColor.darkBlue)
        qp.drawEllipse(int(self.q.x() - r), int(self.q.y() - r), 2 * r, 2 * r)

        qp.end()                                # Delete painter object                            

    def switchDrawing(self):
        if not self.getAddV() and len(self.getPolygons()) > 1:      # Disable editing polygons if more than one polygon exist, user can't choose which one to edit  
            self.messageBox('Operation unavailable', 'Can´t modify polygon when multiple polygons exist.')
        else:
            self.add_vertex = not self.getAddV()                    # Reverse current state if only 1 polygon exists

    def messageBox(self, title: str, text : str) -> None:           
        mb = QMessageBox()
        mb.setWindowTitle(title)
        mb.setText(text)
        mb.exec()                       # Show the object

    def clearData(self):
        self.pol = [[], QPolygonF(), ()]            # clear polygon dict
        self.highlighted.clear()
        self.setPolygons({1 : self.getPol()})        

        self.q.setX(10)       # shift point to upper left corner
        self.q.setY(10)

        self.add_vertex = True

        self.repaint()      

    def getAddV(self):
        return self.add_vertex

    def getWidth(self):
        return self.width()
    
    def getHeight(self):
        return self.height()
    
    def getQ(self):
        return self.q       
    
    def getPol(self):
        return self.pol     
    
    def getPolygons(self):
        return self.polygons   
    
    def getHighlighted(self):
        return self.highlighted  