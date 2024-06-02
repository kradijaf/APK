from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Edge:
    '''
    - class for Delanay triangulation / contour edge
    - is a line segment

    - Methods:
        - __init__(start: QPoint3DF, end: QPoint3DF): a constructor, creates segment´s points
        - changeOrientation() - returns an Edge object with points swapped
        - __eq__(other: Edge) -> bool: compares itself with a given Edge, returns comparison result
        - getter type objects
    '''
    def __init__(self, start: QPoint3DF, end: QPoint3DF) -> None:
        self.start = start
        self.end = end

    def changeOrientation(self):
        return Edge(self.end, self.start)
    
    def __eq__(self, other) -> bool:
        return (self.start == other.start) and (self.end == other.end)
    
    def getStart(self) -> QPoint3DF:
        return self.start
    
    def getEnd(self) -> QPoint3DF:
        return self.end