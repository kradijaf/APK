from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class QPoint3DF(QPointF):
    '''
    - class Inheriting from QPointF, adds Z coordinate as functionality needed for Delanay triangulation.

    - Methods:
        - __init__(x:float, y: float, z: float): a constructor, creates point´s coordinates
        - getZ() -> float: Z coordinate getter
    '''
    def __init__(self, x:float, y: float, z: float) -> None:
        super().__init__(x, y)
        self.z  = z
        
    def getZ(self) -> float:
        return self.z