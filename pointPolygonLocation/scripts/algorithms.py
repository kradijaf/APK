from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import pi, acos
from sys import float_info

class Algorithms:
    '''
    - Class for point-polygon location analysis and other data processing.

    - Methods:
        - __init__(*args, **kwargs) - Creates the Epsilon value
        - rayCrossingAll(q: QPointF, inpt_pols : dict) -> dict - The cumulative function for calling Ray Crossing algorithm, 
            preprocesses data, checks each point-polygon relation, returns polygon that includes the point
        - rayCrossingSingle(q: QPointF, pol: QPolygonF) -> bool - Runs Ray Crossing algorithm for a given polygon, 
            possible outputs: point inside/outside polygon
        - windingNumAll(q: QPointF, inpt_pols : dict) -> dict - The cumulative function for calling Winding Number algorithm
        - windingNumSingle(q: QPointF, pol: QPolygonF) - Runs Winding Number algorithm for a given polygon, 
            possible outputs: point inside/outside polygon, is polygon´s vertex, lays on polygon´s edge
        - get2_LineAngle(p1 : QPointF, p2 : QPointF, p3 : QPointF, p4: QPointF) -> float - Calculates an angle of two lines in radians
        - updateMinMaxBox(polygons : dict)  -> dict - Updates each polygon´s pixel coordinate bounding / min-max box
        - selectInsideBox(q: QPointF, inpt_pols: QPolygonF) -> dict - Select the polygons for whom the point is within their min-max box
        - minMaxBox(polygon: QPolygonF | list) -> tuple - Create´s polygons min-max box
        - sjtsk2Pixel(point : list, width : int, height : int, x_min : float | int, x_max : float | int, y_min : float | int, 
            y_max : float | int) -> tuple - Converts S-JTSK CRS (EPSG: 5514) coordinates to pixel coordinates, stretches them 
            to fill the widget with 5 pixel offset
        - rescale(polygons : dict, w : int, h : int) -> dict - Based on new dimensions, rescales the polygons to fit widget with 5 pixel offset
        - setCCW_Orientation(polygons : dict) -> dict - Tests each polygon´s rotation, sets it to counterclockwise (CCW) if not so
    '''    
    def __init__(self):
        self.EPS = float_info.epsilon ** (1 / 4)         # Equals 4th square root of the smallest possible positive float

    def rayCrossingAll(self, q: QPointF, inpt_pols : dict):

        polygons = self.updateMinMaxBox(inpt_pols)      # Updates each polygon´s min-max box
        polygons = self.selectInsideBox(q, polygons)    # Select the polygons
        polygons = self.setCCW_Orientation(polygons)    # Sets CCW orientation

        true_pols = {}                                  # selected polygons dictionary
        id = 1

        for pol in polygons.values():                   # Test each polygon
            if self.rayCrossingSingle(q, pol):          # Point in polygon
                true_pols.update({id : pol})
                id += 1

        return true_pols

    def rayCrossingSingle(self, q: QPointF, pol: QPolygonF):
        k = 0                                                                   # Initial number of intersections
        pol = pol[1]
        n = len(pol)                                                            # number of polygon´s vertices

        for i in range(n):                                                      # For each edge
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()                                            # Reduce coordinate system to the tested point
            xi1r = pol[(i + 1) % n].x() - q.x()
            yi1r = pol[(i + 1) % n].y() - q.y()                                 # Reduce the next vertex 

            if ((yi1r > 0) and (yir <= 0)) or ((yir > 0) and (yi1r <= 0)):      # Decide if polygon edge is suitable for testing
                xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)                   # Ray-polygon intersection

                if xm > 0:      
                    k += 1                                                      # Increment number of intersection if the intersection lies in right half plane

        if k % 2 == 1:      
            return True                                                         # Point lies in the Polygon if intersections modulo 2 = 1
        else:
            return False       
        
    def windingNumAll(self, q: QPointF, inpt_pols : dict):                             
        polygons = self.updateMinMaxBox(inpt_pols)
        polygons = self.selectInsideBox(q, polygons)
        polygons = self.setCCW_Orientation(polygons)

        true_pols = {}
        pos_meaning = {0 : [], 1 : [], 2 : []}                      # 0: inside the polygon, 1: on its edge, 2: is polygon´s vertex
        id = 1

        for pol in polygons.values():
            location, pnt_pos = self.windingNumSingle(q, pol)       # Outputs = true/false, location number
            if location:
                true_pols.update({id : pol})
                pos_meaning[pnt_pos].append(str(id))         
                id += 1
        return true_pols, pos_meaning

    def windingNumSingle(self, q: QPointF, pol: QPolygonF):
        sum = 0                                                     # Polygon´s winding number
        pol = pol[1]                                                # Qt polygon variable
        n = len(pol)                                                # Number of vertices
        pnt_pos = 0                                                 # location number

        for i in range(n):                                          # For each point in the polygon
            m0 = pol[(i + 1) % n].x() - pol[i % n].x()              # Elements of 't' matrix
            m1 = pol[(i + 1) % n].y() - pol[i % n].y()              
            m2 = q.x() - pol[i % n].x()                             
            m3 = q.y() - pol[i % n].y()

            angle = self.get2_LineAngle(q, pol[(i) % n], q, pol[(i + 1) % n])       # an angle between tested point and vertices of current edge
            if angle == float('Inf'):                                               # tested point one of polygon´s points
                return True, 2
            elif abs(angle - pi) < self.getEps():                                   # tested point lays on polygons edge
                return True, 1

            det = (m0 * m3) - (m1 * m2)                                             # Determinant of 't' matrix
            if det > self.getEps(): 
                plus = True                                                         # Add the angle
            elif det < self.getEps():
                plus = False                                                        # Subtract the angle

            sum += angle if plus else -angle

        if abs(abs(sum) - (2 * pi)) < self.getEps():                                # if sum - 2 * Pi is less than Epsilon, the point lies in the polygon 
            return True, pnt_pos
        else:
            return False, pnt_pos

    def get2_LineAngle(self, p1 : QPointF, p2 : QPointF, p3 : QPointF, p4: QPointF):
        ux = p2.x() - p1.x()                                # create line vector from p1 to p2
        uy = p2.y() - p1.y()

        vx = p4.x() - p3.x()                                # create line vector from p1 to p2
        vy = p4.y() - p3.y()

        dot = ux * vx + uy * vy                             # dot product
        nu = (ux ** 2 + uy ** 2) ** 0.5                     # vector norms
        nv = (vx ** 2 + vy ** 2) ** 0.5
        if (abs(nu) < self.getEps()) or (abs(nv) < self.getEps()):
            return float('Inf')                             # Return infinity if one of vector norms = 0 (Its points are the same)

        return acos(min(max(dot / (nu * nv), -1), 1))       # Return the angle
    
    def updateMinMaxBox(self, polygons : dict):
        for key, pol in polygons.items():
            polygons[key][2] = self.minMaxBox(pol[1])       
        return polygons
    
    def selectInsideBox(self, q: QPointF, inpt_pols: QPolygonF):
        otpt_pols = {}
        id = 1

        x = q.x()
        y = q.y()

        for pol in inpt_pols.values():                                                          # Test each polygon
            box = pol[2]
            x_min = box[0]; x_max = box[1]; y_min = box[2]; y_max = box[3]

            if ((x - x_min == 0) or (x > x_min)) and ((x - x_max == 0) or (x < x_max))\
            and ((y - y_min == 0) or (y > y_min)) and ((y - y_max == 0) or (y < y_max)):        # Point within the box
                otpt_pols.update({id : pol})
                id += 1

        return otpt_pols
        
    def minMaxBox(self, polygon: QPolygonF | list) -> tuple:
        x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')    # Values that will be overwritten on first comparison
        for pnt in polygon:
            try:        
                x = pnt.x()         # Polygon consists of QPointF data type
                y = pnt.y()
            except:
                x = pnt[1]          # Polygon consists of nested lists
                y = pnt[0]

            if x < x_min:
                x_min = x
            elif x > x_max:
                x_max = x
            
            if y < y_min:
                y_min = y
            elif y > y_max:
                y_max = y

        return x_min, x_max, y_min, y_max           
    
    def sjtsk2Pixel(self, point : list, width : int, height : int, x_min : float | int, x_max : float | int, 
                    y_min : float | int, y_max : float | int) -> tuple:        # Used when loading data
        del_pix_x = width - 10                                          # amount of widget´s horizontal pixels used for data
        del_pix_y = height - 10
        del_data_x = abs(x_max - x_min)                                 # data X-coord delta
        del_data_y = abs(y_max - y_min)
        
        x = 5 + abs((point[0] - y_min) / del_data_y) * del_pix_x        # Point´s new coordinates    
        y = 5 + abs((point[1] - x_max) / del_data_x) * del_pix_y        

        return x, y     
    
    def rescale(self, polygons : dict, w : int, h : int):
        polygons = self.updateMinMaxBox(polygons)

        x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')        # bouding box´s inicial values
        for pol in polygons.values():
            box = self.minMaxBox(pol[1])     
            if box[0] < x_min:                                           
                x_min = box[0] - 5
            if box[1] > x_max:
                x_max = box[1] - 5
            if box[2] < y_min:
                y_min = box[2] - 5
            if box[3] > y_max:
                y_max = box[3] - 5

        del_x_old = x_max - x_min                                   # Data´s extent prior to the rescale
        del_y_old = y_max - y_min

        del_x_new = w - 10                                          # New extent to rescale to
        del_y_new = h - 10

        x_axes_ratio = del_x_new / del_x_old                        # axes ratio
        y_axes_ratio = del_y_new / del_y_old

        for key, pol in polygons.items():
            i = 0
            for pnt in pol[1]:                                      # Update each point´s coordinates
                x = 5 + (pnt.x() - 5 - x_min) * x_axes_ratio
                y = 5 + (pnt.y() - 5 - y_min) * y_axes_ratio

                pol[1][i] = QPointF(x, y)                           # Save the point into original data type
                i += 1
            polygons[key][1] = pol[1]       

        return self.updateMinMaxBox(polygons)                       # Return the polygons with updated min-max box
    
    def setCCW_Orientation(self, polygons : dict):                 # Based on equation of polygon area
        for key, pol in polygons.items():
            sum = 0
            n = len(pol[1])                                 # Amount of vertices

            for i in range(1, n + 1):                       # Test each vertex
                sum += (pol[1][i % n].x() * (pol[1][(i - 1) % n].y() - pol[1][(i + 1) % n].y())) * 0.5
            if sum < 0:                                     # Clockwise rotation -> Coordinate reversal
                pnts = [pnt for pnt in pol[1]]
                pnts.reverse()

                polygons[key][1] = QPolygonF(pnts)

                if len(pol[0]) > 0:
                    polygons[key][0].reverse()
            
        return polygons
    
    def getEps(self):
        return self.EPS