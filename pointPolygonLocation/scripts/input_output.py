from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from algorithms import Algorithms
import json

class IO:
    '''
    - Class for data loading and saving. 
    - File dialogs only enable *.TXT, *.GeoJSON and *.TXT files to be the parameters of these functions
        - All files must comply with GeoJSON formatting
    - The program supposes data in S-JTSK CRS (EPSG: 5514)

    - Methods:
        - readPnts(pnt_list : list) -> list - Creates list of doubles of coordinates
        - loadPolygons(file : str, width : int, height : int) -> dict - Loads the data from given file using readPnts() 
            - uses given dimensions for Algorithms.sjtsk2Pixel() to rescale loaded data to widgets dimensions
            - Can load multiple instances of the same point
        - savePolygons(file : str, polygons : dict) -> bool - Saves polygons to given file
            - if real coordinates are saved in the framework, saves them in geometry, then pixel coordinates 
                get saved into features
            - If only pixel coordinates are saved in the framework, saves them as real coordinates
            - Ensures both coordinate types are saved with first and last index containing the same point and having the same length
            - Returns a bool  statement on the result of saving
    ''' 
    def readPnts(self, pnt_list : list):
        coords = []
        while pnt_list:
            part = pnt_list.pop(0)
            while part:
                pnt = part.pop(0)
                if (pnt[0], pnt[1]) not in coords:      # Skip recurring points
                    coords.append((pnt[0], pnt[1]))

        return coords

    def loadPolygons(self, file : str, width : int, height : int) -> list:
        try:
            with open(file, encoding = 'utf-8') as f:       # Open the file
                data = json.load(f)
            
            polygons = {}
            id = 1

            for json_feat in data['features']:              # Extract polygon coordinates
                coords = self.readPnts(json_feat['geometry']['coordinates'])      # extraction of coordinates ignores polygons parts, removes duplicate points
                polygons.update({id : [coords]})
                id += 1

            a = Algorithms()
            x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')        # bouding box´s inicial values
            for pol in polygons.values():
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
            for pol in polygons.values():
                pol_pix_coords = []

                for i in range(len(pol[0])):                # Compute pixel coordinates
                    pol_pix_coords.append(a.sjtsk2Pixel(pol[0][i], width, height, x_min, x_max, y_min, y_max))

                qt_feat = QPolygonF([QPointF(pnt[0], pnt[1]) for pnt in pol_pix_coords])        # Create Qt polygons from pixel coordinates
                for feat in (qt_feat, a.minMaxBox(qt_feat)):
                    polygons[id].append(feat)
                
                id += 1
            return polygons
        except Exception:
            return False

    def savePolygons(self, file : str, polygons : dict):
        try:
            output = {"type" : "FeatureCollection", 
                    "crs" : {
                        "type" : "name",
                        "properties" : {
                            "name" : "EPSG:5514"}},
                    "features" : []}                                                # Create JSON header
            
            save_both = True if polygons[1][0] else False                           # Save both types of coordinates if both types exist in data
            id = 1

            for pol in polygons.values():
                feat = {'type' : 'Feature', 
                        'id' : id, 
                        'geometry' : {
                            'type' : 'Polygon'}}                                    # Create feature header
                coords = [pol[0]] if save_both else [[[pnt.x(), pnt.y()] for pnt in pol[1]]]
                attributes = {'pixel_coordinates' : [[[pnt.x(), pnt.y()] for pnt in pol[1]]]} if save_both else {}

                if coords[0][0] and (coords[0][0][0] != coords[0][0][-1]):          # append first coordinate to real coordinates if last point doesn't equal it
                    if save_both:
                        coords[0].append(pol[0][0])
                    else:
                        coords[0].append([pol[1][0].x(), pol[1][0].y()])
                if attributes and (attributes['pixel_coordinates']) and (attributes['pixel_coordinates'][0][0][0] != attributes['pixel_coordinates'][0][0][-1]):
                    attributes['pixel_coordinates'][0].append(attributes['pixel_coordinates'][0][0])        # append first coordinate to pixel coordinates (in properties) if last point doesn't equal it

                feat['geometry'].update({'coordinates' : coords})                   # append coordinate dictionaries to feature
                feat.update({'properties' : attributes})

                output['features'].append(feat)                                     # append feature to output dict

                id += 1

            with open(file, 'w', encoding = 'utf-8') as f:                          # Save the file
                json.dump(output, f, indent = 2)
            return True
        except Exception:
            return False