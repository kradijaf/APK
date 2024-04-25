from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from algorithms import Algorithms
import json
from prettytable import PrettyTable

class IO:
    '''
    - Class for data loading and saving data. 
    - Load file dialog only accepts *.TXT, *.GeoJSON and *.JSON files 
        - Loads files with GeoJSON formatting
    - Load file dialog only accepts *.TXT files
    - The program supposes data in S-JTSK CRS (EPSG: 5514)

    - Methods:
        - readPnts(pnt_list: list) -> list - Creates list of tuples of coordinates
        - loadBlds(file: str, width: int, height: int) -> dict - Loads the data from given file using readPnts() 
            - uses given dimensions for Algorithms.sjtsk2Pixel() to rescale loaded data to widgets dimensions,
            - loads multiple instances of the same point
        - saveTable(file: str, table: PrettyTable) -> bool - saves main direction efficiency statistics stable
            - Returns a bool statement on the result of saving
    ''' 
    def readPnts(self, pnt_list : list) -> list:
        coords = []
        while pnt_list:             # while unread data exist
            part = pnt_list.pop(0)
            while part:
                pnt = part.pop(0)
                coords.append((pnt[0], pnt[1]))

        return coords

    def loadBlds(self, file : str, width : int, height : int) -> dict:
        try:
            with open(file, encoding = 'utf-8') as f:       # Open the file
                data = json.load(f)
            
            blds = {}                                       # read buildings
            id = 1

            for json_feat in data['features']:              # Extract buildings´ coordinates
                coords = self.readPnts(json_feat['geometry']['coordinates'])      # extraction of coordinates ignores polygons parts, keeps duplicate points
                blds.update({id : [coords]})
                id += 1

            a = Algorithms()
            x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')        # bouding box´s inicial values
            for pol in blds.values():
                box = a.minMaxBox(pol[0])     
                if box[0] < x_min:                                           
                    x_min = box[0]
                if box[1] > x_max:
                    x_max = box[1]
                if box[2] < y_min:
                    y_min = box[2]
                if box[3] > y_max:
                    y_max = box[3]

            id = 1
            for pol in blds.values():                       # For each building loaded
                pol_pix_coords = []

                for i in range(len(pol[0])):                # Compute pixel coordinates
                    pol_pix_coords.append(a.sjtsk2Pixel(pol[0][i], width, height, x_min, x_max, y_min, y_max))
                blds[id] = QPolygonF([QPointF(pnt[0], pnt[1]) for pnt in pol_pix_coords])       # Replace absolute coordinates with pixel coordinates Qt polygon
                id += 1
            
            return blds
        except Exception:
            return False
        
    def saveTable(self, file : str, table : PrettyTable) -> bool:
        try:
            with open(file, 'w', encoding = 'utf-8') as f:              # Open the file
                f.write(table.get_string())                             # Save the table converted to string
            return True
        except Exception:
            return False