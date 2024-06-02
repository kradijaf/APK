from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
from scipy.linalg import *
from qpoint3df import QPoint3DF
from edge import *
from triangle import *

class Algorithms:
    '''
    - class for generating DT and analysis of it

    - Methods:
        - get2LineAnglep1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF) -> float: computes an angle between 2 given line segments
        - getPointAndLinePosition(p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF) -> int: computes line segment - point relationship: 
            - 1 = Point in the left half plane
            - 0 = Point in the right half plane
            - -1 = Point on the line
        - getNearestPoint(q:QPoint3DF, points:list[QPoint3DF]) -> QPoint3DF: Find point nearest to q
        - twoPointDist(from_p: QPoint3DF, to_p: QPoint3DF) -> tuple [float, float]: return X and Y coordinate directions between 2 given points
        - getDelaunayPoint(start:QPoint3DF,end:QPoint3DF, points:list[QPoint3DF]) -> QPoint3DF: Find Delaunay point to an edge
        - updateAEL(e: Edge, ael: list[Edge]): update given active edges list
        - createDT(points: list[QPoint3DF]) -> list[Edge]: Create Delaunay triangulation with incremental method
        - getContourPoint(p1:QPoint3DF, p2:QPoint3DF, z:float) -> QPoint3DF: compute an intersection of triangle and horizontal plane:
        - createContourLines(dt: float, zmin: float, zmax: float, dz: float) -> list[Edge]: Create contour lines defined by interval and step
        - computeSlope(p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF) -> float: compute triangle´s slope
        - computeAspect(sp1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF) -> float: compute triangle´s aspect
        - normalsVectors(p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF) -> tuple[float, float, float]: compute X, Y, Z directions of a vector normal to plane created by 3 given points
        - analyzeDTMSlope(dt: list[Edge]) -> list[Triangle]: compute triangle´s slope [rad]
        - analyzeDTMAspect(dt: list[Edge]) -> list[Triangle]: compute triangle´s aspect [rad]
        - sjtsk2Pixel(pnt : list, width : int, height : int, x_min : float, x_max : float, y_min : float, y_max : float) -> tuple[float, float]: computes S-JTSK CRS (EPSG: 5514) 
            coordinates to pixel coordinates, stretches them to fill the widget with 5 pixel offset
        - uniquePerDim(points: list) -> tuple[int, int]: returns count of unique coordinates in X and Y axis separately
        - rescale(points: list, dt: list, contours: list, slope: list, aspect: list, w : int, h : int) -> list[QPoint3DF]: Based on new dimensions, rescales all data to fit canvas with 5 pixel offset 
        - rescaledCoords(pnt: QPoint3DF, x_min: float, y_min: float, del_pix_x: int, del_pix_y: int, del_data_x: float, del_data_y: float) -> tuple[float, float]: computes rescaled coords in rescale()
            - uses slightly different equation than sjtsk2Pixel()
    '''
    def get2LineAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF) -> float:
        ux, uy = self.twoPointDist(p1, p2)          # point distances/vectors         
        vx, vy = self.twoPointDist(p3, p4)

        dot = ux * vx + uy * vy                     #Dot product
        
        nu = (ux**2 + uy**2)**(1/2)
        nv = (vx**2 + vy**2)**(1/2)                 #Vector norms
        
        arg = dot/(nu*nv)                           #Correct interval
        return acos(max(min(arg, 1), -1))
   
    def getPointAndLinePosition(self, p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF) -> int: 
        ux, uy = self.twoPointDist(p1, p2)          # point distances/vectors   
        vx, vy = self.twoPointDist(p1, p)
        
        t = ux*vy - uy*vx                           #Compute test
        
        if t > 0:
            return 1                                #Point in the left half plane
        elif t < 0:
            return 0                                #Point in the right half plane
        return -1                                   #Point on the line
    
    def getNearestPoint(self, q:QPoint3DF, points:list[QPoint3DF]) -> QPoint3DF:
        p_nearest = None
        dist_nearest = inf
        
        for p in points:                            #Process all points
            if p!=q:                                #Point p differentiates from q    
                dx, dy = self.twoPointDist(q, p)            #Compute distance
                dist = sqrt(dx**2 + dy**2)
                
                if dist < dist_nearest:             #Update nearest point
                    p_nearest = p
                    dist_nearest = dist

        return p_nearest

    def twoPointDist(self, from_p: QPoint3DF, to_p: QPoint3DF) -> tuple [float, float]:
        x = to_p.x() - from_p.x()                   # X coordinate vector/distance
        y = to_p.y() - from_p.y()                   # Y coordinate vector/distance

        return x, y

    def getDelaunayPoint(self, start:QPoint3DF,end:QPoint3DF, points:list[QPoint3DF]) -> QPoint3DF:
        p_dt = None
        angle_max = 0   
             
        for p in points:         
            #Point p differentiates from q and is in the left halfplane:
            if (start != p and end != p) and (self.getPointAndLinePosition(p, start, end) == 1):                                         
                angle = self.get2LineAngle(p, start, p, end)                #Compute angle

                if angle > angle_max:                                       # Update maximum
                    angle_max = angle
                    p_dt = p
        
        return p_dt
    
    def updateAEL(self, e: Edge, ael: list[Edge]) -> None:
        e_op = e.changeOrientation()            #Update active edges list

        if e_op in ael:                         #Is edge in ael?
            ael.remove(e_op)                    #Remove edge   
        else:                                   #Add edge to ael
            ael.append(e)        
                
    def createDT(self, points: list[QPoint3DF]) -> list[Edge]:
        dt = []
        ael = []

        p1 = min(points, key = lambda k: k.x())     # point with smallest x coordinate 
        p2 = self.getNearestPoint(p1, points)       # Find nearest point to p1
        
        e = Edge(p1, p2)                            #Create edge
        e_op = Edge(p2, p1)                         # opposite edge
        
        ael.append(e)
        ael.append(e_op)                            #Add both edges to ael
        
        while ael:                                  # Repeat until ael is empty
            e1 = ael.pop()                          # Take first edge
            e1_op = e1.changeOrientation()          #Change orientation
            
            p_dt = self.getDelaunayPoint(e1_op.getStart(), e1_op.getEnd(), points)          #Find optimal Delaunay point
            if p_dt != None:                        #Did we find a suitable point?
                e2 = Edge(e1_op.getEnd(), p_dt)
                e3 = Edge(p_dt, e1_op.getStart())   #create remaining edges
                
                dt.append(e1_op)
                dt.append(e2)
                dt.append(e3)                       #Create Delaunay triangle
                
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)             #Update AEL
                
        return dt
    
    def getContourPoint(self, p1:QPoint3DF, p2:QPoint3DF, z:float) -> QPoint3DF:
        xb = (p2.x() - p1.x())/(p2.getZ()-p1.getZ()) * (z-p1.getZ()) + p1.x()
        yb = (p2.y() - p1.y())/(p2.getZ()-p1.getZ()) * (z-p1.getZ()) + p1.y()
        
        return QPoint3DF(xb, yb, z)
    
    def createContourLines(self, dt: float, zmin: float, zmax: float, dz: float) -> list[Edge]:
        contours = []  
        
        for i in range(0, len(dt), 3):                      #Process all triangles
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i + 1].getEnd()                         #Get vertices of triangle
            
            z1 = p1.getZ()
            z2 = p2.getZ()
            z3 = p3.getZ()                                  #Get z coordinates
            
            for z in np.arange(zmin, zmax, dz):             #Create all contour lines
                dz1 = z - z1
                dz2 = z - z2
                dz3 = z - z3                                #Compute edge height differences
                
                if dz1 == 0 and dz2 == 0 and dz3 == 0:      #skip coplanar triangle
                    continue
                
                elif dz1 ==0 and dz2 ==0:                   #Edges p1 and p2 are colinear
                    contours.append(dt[i])
                
                elif dz2 ==0 and dz3==0:                    #Edges p2 and p3 are colinear
                    contours.append(dt[i+1]) 
                
                elif dz3 ==0 and dz1==0:                    #Edges p3 and p1 are colinear
                    contours.append(dt[i+2]) 
                    
                elif dz1 * dz2 <= 0 and dz2 * dz3 <= 0:     #Edges p1, p2 and p2, p3 intersected by plane
                    a = self.getContourPoint(p1, p2, z)
                    b = self.getContourPoint(p2, p3, z)     #Compute intersections

                    e1 = Edge(a, b)                         #Create edge
                    contours.append(e1)                     #Add edge to contour lines
                
                elif dz2 * dz3 <= 0 and dz3 * dz1 <= 0:     #Edges p2, p3 and p3, p1 intersected by plane
                    a = self.getContourPoint(p2, p3, z)
                    b = self.getContourPoint(p3, p1, z)     #Compute intersections
                    
                    e1 = Edge(a, b)                         #Create edge
                    contours.append(e1)                     #Add edge to contour lines
                
                elif dz3 * dz1 <= 0 and dz1 * dz2 <= 0:     #Edges p3, p1 and p1, p2 intersected by plane
                    a = self.getContourPoint(p3, p1, z)
                    b = self.getContourPoint(p1, p2, z)     #Compute intersections
                    
                    e1 = Edge(a, b)                         #Create edge
                    contours.append(e1)                     #Add edge to contour lines
                
        return contours
    
    def computeSlope(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF) -> float:
        nx, ny, nz = self.normalsVectors(p1, p2, p3)            #Normal vector  
        norm = (nx ** 2 +ny ** 2 + nz ** 2) ** (1/2)            #Norm

        return acos(abs(nz)/norm)        
           
    def computeAspect(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF) -> float:
        nx, ny, tmp = self.normalsVectors(p1, p2, p3)           #Normal vector  
        return atan2(nx, ny) 

    def normalsVectors(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF) -> tuple[float, float, float]:
        ux = p1.x() - p2.x() 
        uy = p1.y() - p2.y() 
        uz = p1.getZ() - p2.getZ()                      # p1 to p2 distance/vector               
        
        vx = p3.x() - p2.x() 
        vy = p3.y() - p2.y() 
        vz = p3.getZ() - p2.getZ()                      #p2 to p3 distance/vector 
        
        nx = uy * vz - vy * uz
        ny = - (ux*vz - vx * uz)
        nz = ux * vy - vx * uy                          #Normal vector

        return nx, ny, nz       
                
    def analyzeDTMSlope(self, dt: list[Edge]) -> list[Triangle]:
        dtm_slope: list [Triangle] = []    
        
        for i in range(0, len(dt), 3):                          #Process all triangles
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i + 1].getEnd()                             #Get vertices of triangle
            
            slope = self.computeSlope(p1, p2, p3)               #Get slope
            triangle = Triangle(p1, p2, p3, slope, 0)           #Create triangle
            dtm_slope.append(triangle)                          #Add triangle to the list
            
        return dtm_slope
    
    def analyzeDTMAspect(self, dt: list[Edge]) -> list[Triangle]:
        dtm_aspect: list [Triangle] = []    
        
        for i in range(0, len(dt), 3):                          #Process all triangles
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i + 1].getEnd()                             #Get vertices of triangle
            
            aspect = self.computeAspect(p1, p2, p3)             #Get aspect
            triangle = Triangle(p1, p2, p3, 0, aspect)          #Create triangle
            dtm_aspect.append(triangle)                         #Add triangle to the list
            
        return dtm_aspect
    
    def sjtsk2Pixel(self, pnt : list, width : int, height : int, x_min : float, x_max : float, y_min : float, y_max : float) -> tuple[float, float]:        
        del_pix_x = width - 10                                                  # amount of widget´s horizontal pixels used for data
        del_pix_y = height - 10

        del_data_x = abs(x_max - x_min)                                         # data X-coord delta
        del_data_y = abs(y_max - y_min)    

        x = 5 + ((abs(pnt[0] - x_min) * (del_pix_x)) / (del_data_x))            # Point´s new coordinates
        y = 5 + ((abs(pnt[1] - y_max) * (del_pix_y)) / (del_data_y))

        return x, y 
    
    def uniquePerDim(self, points: list) -> tuple[int, int]:
        pnt_array = np.array([[pnt.x(), pnt.y()] for pnt in points])            # create array indexable in both dimensions

        unique_x = len(np.unique(pnt_array[:, : 1]))
        unique_y = len(np.unique(pnt_array[:, 1 : 2]))

        return unique_x, unique_y

    def rescale(self, points: list, dt: list, contours: list, slope: list, aspect: list, w : int, h : int) -> list[QPoint3DF]:
        new_points, new_dt, new_contours, new_slope, new_aspect = [], [], [], [], []

        # get coordinates of input data´s bounding box (point cloud is enough for maximal/minimal coordinates retrieval):
        x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')        # bouding box´s inicial values

        for pnt in points:
            x = pnt.x()
            y = pnt.y()

            if x < x_min:
                x_min = x
            elif x > x_max:
                x_max = x
            
            if y < y_min:
                y_min = y
            elif y > y_max:
                y_max = y

        del_pix_x = w - 10                      # amount of widget´s horizontal pixels used for data
        del_pix_y = h - 10

        del_data_x = abs(x_max - x_min)         # data X-coord delta
        del_data_y = abs(y_max - y_min)

        for pnt in points:                      # set point cloud´s new coordinates      
            x, y = self.rescaledCoords(pnt, x_min, y_min, del_pix_x, del_pix_y, del_data_x, del_data_y)
            new_points.append(QPoint3DF(x, y, pnt.getZ()))

        # set dt´s and contours´ new coordinates:
        edge_lists = (dt, contours)                             
        new_edge_lists = (new_dt, new_contours)         # auxilliary variables for usage in for-cycle

        for i in range(2):
            for edge in edge_lists[i]:          # compute edge´s new coordinates
                tmp = []                        # edge´s temporary point container

                for pnt in (edge.getStart(), edge.getEnd()):
                    x, y = self.rescaledCoords(pnt, x_min, y_min, del_pix_x, del_pix_y, del_data_x, del_data_y)
                    tmp.append(QPoint3DF(x, y, None))
                
                new_edge_lists[i].append(Edge(tmp[0], tmp[1]))          # place new edge into it´s new list

        # set slope´s and aspect´s new coordinates:         
        triangle_lists = (slope, aspect)
        new_triangle_lists = (new_slope, new_aspect)

        for i in range(2):
            for triangle in triangle_lists[i]:          # compute triangle´s new coordinates
                tmp = []                                # triangle´s temporary point container

                for pnt in triangle.getVertices():
                    x, y = self.rescaledCoords(pnt, x_min, y_min, del_pix_x, del_pix_y, del_data_x, del_data_y)
                    tmp.append(QPoint3DF(x, y, None))
                
                new_triangle = (Triangle(tmp[0], tmp[1], tmp[2], triangle.getSlope(), 0)) if i == 0 else (Triangle(tmp[0], tmp[1], tmp[2], 0, triangle.getAspect()))
                new_triangle_lists[i].append(new_triangle)              # place new triangle into it´s new list         

        return new_points, new_dt, new_contours, new_slope, new_aspect                                         
                
    def rescaledCoords(self, pnt: QPoint3DF, x_min: float, y_min: float, del_pix_x: int, del_pix_y: int, del_data_x: float, del_data_y: float) -> tuple[float, float]:
        x = 5 + ((abs(pnt.x() - x_min) * (del_pix_x)) / (del_data_x))
        y = 5 + ((abs(pnt.y() - y_min) * (del_pix_y)) / (del_data_y))

        return x, y
