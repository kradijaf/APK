from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Triangle:
    '''
    - class for slope / aspect analysis, can store both features, used for one at a time

    - Methods:
        - __init__(p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF, slope: float, aspect: float): a constructor, creates QPolygonF of triangle´s points, slope/aspect value
        - getter type objects
    '''
    def __init__(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF, slope: float, aspect: float) -> None:
        self.vertices = QPolygonF([p1, p2, p3])
        
        self.slope = slope
        self.aspect = aspect
        
    def getVertices(self) -> QPolygonF:
        return self.vertices
    
    def getSlope(self) -> float:
        return self.slope
    
    def getAspect(self) -> float:
        return self.aspect