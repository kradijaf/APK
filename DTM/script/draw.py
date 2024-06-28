from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import QPoint3DF
from edge import *
from random import *
from triangle import *
from math import *

class Draw(QWidget):
    '''
    - a class for program´s graphical operations.

    - Methods:
        - __init__(*args, **kwargs): the constructor with default parameters necessary for Qt, sets up the framework for drawing on the widget
            - creates empty list for each feature related to DT
        - mousePressEvent(e:QMouseEvent): Reacts to mouse click on widget -> draws a point, with a random Z coordinate from <195; 1000> m interval
        - messageBox(title: str, text : str): Creates a message box with given text
        - paintEvent(e: QPaintEvent): Refreshes the widget: draws point cloud, DT, contours, slope and aspect
            - draws slope using continuous gray color ramp with RGB model 
            - draws aspect using graduated color spectrum ramp with HSV model 
        - aspectByInterval(aspect: float): transforms aspect value to match ESRI (2024), finds matching aspect interval, returns interval´s hue

        - clear type functions:
            - both reset canvas to initial state

            - clearAll(): clear results and input data
            - clearResults(): clear results

        - getter type functions
        - setter type functions
    '''
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.points, self.dt, self.contours, self.dtm_slope, self.dtm_aspect = [], [], [], [], []
        # initial state equals unchecked options in "View" pane:
        self.viewDT, self.viewContourLines, self.viewSlope, self.viewAspect = False, False, False, False               

    def mousePressEvent(self, e:QMouseEvent) -> None:
        x = e.position().x()                    #Get cursor position
        y = e.position().y()
        
        ZMIN, ZMAX = 195, 1000
        z = random() * (ZMAX - ZMIN) + ZMIN     #Generate random height
        
        p = QPoint3DF(x, y, z)                  #Create new point
        self.points.append(p)                   #Add point to the point cloud

        self.repaint()                          #Repaint screen

    def messageBox(self, title: str, text : str) -> None:           
        mb = QMessageBox()
        mb.setWindowTitle(title)
        mb.setText(text)
        mb.exec()   
        
    def paintEvent(self, e: QPaintEvent) -> None:
        #Draw situation
        qp = QPainter(self)                         #Create new object

        if self.viewSlope:                          
            qp.setPen(Qt.GlobalColor.gray)          #Set graphic attributes
            for t in self.dtm_slope:                #Draw slope
                slope = t.getSlope()                #Get slope

                mju = 2 * 255 / pi
                col = int(255 - mju * slope)        #Convert slope to color
                color = QColor(col, col, col)

                qp.setBrush(color)
                qp.drawPolygon(t.getVertices())     #Draw slope

        if self.viewAspect:                         
            qp.setPen(Qt.GlobalColor.gray)          #Set graphic attributes          

            for t in self.dtm_aspect:               #Draw aspect
                aspect = degrees(t.getAspect())            # convert aspect to degrees
                hue = self.aspectByInterval(aspect)
                color = QColor().fromHsvF(hue / 360, 0.9, 0.95)      

                qp.setBrush(color)
                qp.drawPolygon(t.getVertices())     #Draw aspect

        if self.viewDT:                                
            qp.setPen(Qt.GlobalColor.green)
            qp.setBrush(Qt.GlobalColor.transparent)         #Set graphic attributes

            for e in self.dt:                       #Draw triangulation
                qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        if self.viewContourLines:                   
            qp.setPen(QColor(191, 115, 38))

            for e in self.contours:                 #Draw contour lines
               qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        r = 2
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        for p in self.points:                       #Draw points
            qp.drawEllipse(int(p.x()-r), int(p.y()-r), 2*r, 2*r)

        qp.end()                                    #End drawing

    def aspectByInterval(self, aspect: float):
        aspect %= 360
        aspect = 360 - aspect                       # shift and change aspect orientation to CW where (0; 1) = 0° (matches orientation as in ESRI (2024))

        int_centers_colors = {0 : 0,
                              45 : 39,
                              90 : 60,
                              135 : 120,
                              180 : 180,
                              225 : 201,
                              270 : 240,
                              315 : 300,
                              360 : 0}              # aspect interval´s center : interval color´s hue (hue matches hues in ESRI (2024))
        int_center = min(int_centers_colors.keys(), key = lambda x: abs(x - aspect))            # select center closest to aspect
        
        return int_centers_colors[int_center]       # return interval´s hue

    def clearAll(self) -> None:
        self.points.clear()                         #Clear points
        self.clearResults()                         #Clear results
        self.repaint()                              #Repaint screen
        
    def clearResults(self) -> None:
        self.dt.clear()                             #Clear DT
        self.contours.clear()                       #Clear contours
        self.dtm_slope.clear()                      #Clear slope
        self.dtm_aspect.clear()                     #Clear aspect

        self.repaint()                              #Repaint screen   
        

    def getPoints(self) -> list[QPoint3DF]:
        return self.points                          
    
    def getDT(self) -> list[Edge]:
        return self.dt                               

    def getContours(self) -> list[Edge]:
        return self.contours                       

    def getDTMAspect(self) -> list[Triangle]:
        return self.dtm_aspect                  
    
    def getDTMSlope(self) -> list[Triangle]:
        return self.dtm_slope                
    
         
    def getWidth(self) -> int:
        return self.width()
    
    def getHeight(self) -> int:
        return self.height()     
    

    def setPoints(self, points: list[QPoint3DF]) -> None:
        self.points = points
    
    def setDT(self, dt: list[Edge]) -> None:
        self.dt = dt
        
    def setContours(self, contours: list[Edge]) -> None:
        self.contours = contours

    def setDTMAspect(self, dtm_aspect: list[Triangle]) -> None:
        self.dtm_aspect = dtm_aspect    
    
    def setDTMSlope(self, dtm_slope: list[Triangle]) -> None:
        self.dtm_slope = dtm_slope

    
    def setViewDT(self, viewDT: bool) -> None:
        self.viewDT = viewDT  
        
    def setViewContourLines(self, viewContourLines: bool) -> None:
        self.viewContourLines = viewContourLines       
        
    def setViewSlope(self, viewSlope: bool) -> None:
        self.viewSlope = viewSlope    
        
    def setViewAspect(self, viewAspect: bool) -> None:
        self.viewAspect = viewAspect