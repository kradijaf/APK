from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from algorithms import Algorithms
from qpoint3df import QPoint3DF
import json

class IO:
    '''
    - Class for data loading data. 
    - Load file dialog only accepts *.TXT, *.GeoJSON and *.JSON files 
        - Loads files with GeoJSON formatting
    - The program supposes data in S-JTSK CRS (EPSG: 5514)

    - Methods:
        - load(file: str, width: int, height: int) -> list[QPoint3DF] | bool - Loads the data from given file 
            - uses given dimensions for Algorithms.sjtsk2Pixel() to rescale loaded data to widgets dimensions,
            - loads a single instances of a duplicate point
    ''' 

    def load(self, file : str, width : int, height : int) -> list[QPoint3DF] | bool:
        try:
            with open(file, encoding = 'utf-8') as f:           # Open the file
                data = json.load(f)
            
            points = []                                         # processed points
            for json_feat in data['features']:                  # Extract point´s coordinates
                coords = json_feat['geometry']['coordinates']   # ignore duplicate points
                if coords not in points:
                    points.append(coords)

            if len(points) == 0:
                return False                                    # exit if no features were loaded

            a = Algorithms()
            x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')            # bounding box´s inicial values

            for pnt in points:                                  # determine min/max coordinates
                x = pnt[0]
                y = pnt[1]

                if x < x_min:
                    x_min = x
                elif x > x_max:
                    x_max = x
                
                if y < y_min:
                    y_min = y
                elif y > y_max:
                    y_max = y

            pix_coords = []
            for pnt in points:                     
                x, y = a.sjtsk2Pixel(pnt, width, height, x_min, x_max, y_min, y_max)            # Compute pixel coordinates
                pix_coords.append(QPoint3DF(x, y, pnt[2]))
            
            return pix_coords
        
        except Exception:
            return False