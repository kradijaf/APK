from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from sys import float_info
import numpy as np
import scipy.linalg as spl
from prettytable import PrettyTable
from typing import Callable

EPS = float_info.epsilon * 100          # machine epsilon = smallest possible positive float * 100

class InvalidBldError(Exception):       # Error class code called one a building given to a generalization algorithm has less than 3 unique vertices
    pass

class FrameworkError(Exception):        # error class called when MAER algorithm crashes
    count = 0

    def __init__(self) -> None:
        pass

    def increment() -> None:            # Increase the counter by 1
        FrameworkError.count += 1

    def resetCount() -> None:           # Reset the counter
        FrameworkError.count = 0

    def getCount() -> int:              # Number of buildings for which the calculation crashed
        return FrameworkError.count

class Algorithms:
    '''
    - Class for building generalization and other data processing.

    - Methods:
        - generalize(algo : Callable, blds : dict) -> dict - calls given MBR algorithm for each preprocessed building, quits if any building has less < 3 unique vertices
            - Continues if MEAR algorithm crashes on given building
            - all algorithms called by this function have the same input and outputs: (bld : QPolygonF) -> QPolygonF
                - MAER() - Uses Graham scan algorithm for creating convex hull
                - PCA() - Computes MBR using Principal Component Analysis
                - LE() - Computes MBR using Longest Edge algorithm
                - WA() - Computes MBR using Wall Average algorithm
                - WB() - Computes MBR using Weighted bisector algorithm
                    - uses input polygon´s two longest edges as selected diagonals if given polygon is a triangle
                    - computes all CCW oriented diagonals if input polygon is not a triangle, the algorithm prefers diagonals lying inside the polygon
                        - If a diagonal doesn't intersect any of polygon´s edges, it's center is tested for position purely inside polygon using Winding Number algorithm, 
                        if tested positive, the diagonal is classified as inside the polygon
                    - algorithm selects two longest diagonals, inside the polygon if possible 
        - LE_Sigma(bld : QPolygonF) -> float - Find building´s longest edge and it´s sigma, used by Longest Edge algorithm
        - MBR_FromSigma(bld : QPolygonF, sigma : float) -> QPolygonF) - Creates MBR from given building and it´s sigma, used in all MBR algorithms
        - innerDiags(bld : QPolygonF, diags : dict) -> tuple[list, list]) - Sort diagonals of given building into collections of diagonals inside/outside given building
            - Used by Weighted Bisector algorithm
        - windingNum(bld: QPolygonF, q: QPointF) -> bool - Runs Winding Number algorithm for a given building and a point, 
            - Returns positive result only if point doesn't lay outside, on building´s edge or is not equal to a vertex of the building
        - rateAll(blds : dict, mbrs : dict, common_k : set) -> tuple[PrettyTable, tuple] - Computes MBR´s main direction detection efficiency for each building-MBR pair
            - returns sigma1 and sigma2 table and its summary statistics
        - rateSingle(bld : QPolygonF, mbr : QPolygonF) -> tuple[float, float] - Compute the efficiency for a single building-MBR pair
        - R(sig : float) -> float - Computes the R Constant of given MBR's sigma, used for comparing it to the building in rateSingle()
        - fineCount(values : list) -> int: - Returns number of values in input list lower than 10
            - Used in efficiency rating algorithm (rateSingle())
        - grahamScan(bld : QPolygonF) -> QPolygonF - Computes complex hull using Graham scale algorithm, returns strict convex hull
            - half plane test of its star-shaped polygon is where MAER algorithm crashes
        - get_2line_angle(p_from : QPointF, p_to : QPointF, p_from1 : QPointF, p_to1: QPointF) -> float - Calculates an angle of two lines in radians 
        - starShapedPolygon(bld: QPolygonF) -> QPolygonF - Creates star shaped polygon from input building, Removes a duplicate point if two adjacent points have the same angle
        - rotate(mmb : QPolygonF | tuple, sig : float) -> QPolygonF - Rotates given Min-Max Box by given angle
        - getArea(bld : QPolygonF | tuple) -> float - Computes input buildings area [pixel coordinates]
        - setInputPol(pol : QPolygonF | tuple) -> QPolygonF - starting from lower right corner, creates CCW oriented QPolygonF from Given Polygon is a Min-Max Box (tuple)
            - Used in rotate() and getArea() 
        - resizeRect(mmb: QPolygonF, build: QPolygonF) -> QPolygonF - Resizes given Min-Max Box to match input building´s area
        - setCCW_Orientation(blds : dict) -> dict - Tests each polygon´s rotation, sets it to counterclockwise (CCW) if not so 
        - removeDupl(blds : dict) -> dict) - Returns given building with unique points only
        - strictC_Hull(ch : QPolygonF) -> QPolygonF - Transforms given convex hull to a strict one
        - halfPlaneTest(p_from : QPointF, p_to: QPointF, p_test: QPointF) -> float - Returns half plane test´s determinant
        - minMaxBox(polygon: QPolygonF | list) -> tuple - Creates Min-Max Box of input building
        - coordDiffDist(p1 : QPointF, p2 : QPointF) -> tuple[float, float, float] - Computes coordinate distance in each dimension and their euclidian distance
        - sjtsk2Pixel(point : list, width : int, height : int, x_min : float, x_max : float, y_min : float, y_max : float) -> tuple: 
            - Converts S-JTSK CRS (EPSG: 5514) coordinates to pixel coordinates, stretches them to fill the widget with 5 pixel offset
        - rescaleAll(blds : dict, mbrs : dict, w : int, h : int) -> tuple [dict, dict] - Based on new dimensions, rescales Buildings and MBRs to fit widget with 5 pixel offset 
    '''    
    def generalize(self, algo : Callable, blds : dict) -> dict:
        blds_copy = {key : val[ : ] for key, val in blds.items()}           # A physical copy          
        blds_copy = self.removeDupl(blds_copy)                              # Remove duplicate points

        for bld in blds.values():
            if len(bld) < 3:                                                # A polygon with less than 3 vertices occured
                raise InvalidBldError

        blds_copy = self.setCCW_Orientation(blds_copy)                      # Ensure all polygons have the same orientation
        mbrs = {}                                                           # selected polygons dictionary
        id = 1

        for bld in blds_copy.values():                                      # Test each polygon
            try:
                mbrs.update({id : algo(bld)})
            except FrameworkError:                                          # MAER algorithm crashed
                FrameworkError.increment()
                continue
            finally:                            
                id += 1                                                     # Increment ID so next computed MBR matches its building´s id

        return mbrs    

    def MAER(self, bld : QPolygonF) -> QPolygonF:
        ch = self.grahamScan(bld)                                           # compute convex hull
        mmb_min = self.minMaxBox(ch)                                        # initial min-max box
        area_min = self.getArea(mmb_min)                                    # initial minimal area
        sigma_min = 0                                                       # initial an angle between ch´s and polygon´s edge

        n = len(ch)                                                         # amount of vertices
        for i in range(n):                                                  # process all vertices
            dx, dy, tmp = self.coordDiffDist(ch[i], ch[(i + 1) % n])        # Compute coordinate distances

            sigma = atan2(dy, dx)                                           # the angle between ch´s and polygon´s edge 
            ch_rot = self.rotate(ch, -sigma)                                # rotate convex hull by -sigma

            mmb_rot = self.minMaxBox(ch_rot)                                # compute current ch´s min-max box and area
            area_rot = self.getArea(mmb_rot)

            if area_rot < area_min:                                         # If smaller MBR was found
                mmb_min = mmb_rot                                           # update current min-max box, minimal area and sigma
                area_min = area_rot
                sigma_min = sigma

        mmb_unrot = self.rotate(mmb_min, sigma_min)                         # rotate minimum bounding rectangle to offset the last rotation
        return self.resizeRect(mmb_unrot, bld)                              # resize minimum bounding rectangle to match input building´s area     

    def PCA(self, bld : QPolygonF) -> QPolygonF:
        P = np.array([[pnt.x() for pnt in bld], [pnt.y() for pnt in bld]])      # input polygon´s x, y coords array
        C = np.cov(P)                                                           # compute covariation matrix                                 
        [U, S, V] = spl.svd(C)                                                  # singular value decomposition

        sigma = atan2(U[0][1], U[0][0])                                         # compute sigma                                       
        return self.MBR_FromSigma(bld, sigma)                                   # Create MBR from given building and its sigma
    
    def LE(self, bld : QPolygonF) -> QPolygonF:
        bld_copy = bld[ : ]                             # A physical copy  

        sigma = self.LE_Sigma(bld_copy)                 # building´s longest edge´s sigma 
        return self.MBR_FromSigma(bld_copy, sigma)

    def WA(self, bld : QPolygonF) -> QPolygonF:   
        sigma = 0
        bld_copy = bld[ : ]
        n = len(bld_copy)

        for i in range(n):
            p1 = bld_copy[i - 1]                                # Previous point
            p2 = bld_copy[i]                                    # Current point
            p3 = bld_copy[(i + 1) % n]                          # next point

            dx1, dy1, tmp = self.coordDiffDist(p1, p2)          
            dx2, dy2, edge_len = self.coordDiffDist(p2, p3)

            sigma1 = atan2(dy1, dx1)                            # vertice´s sigmas to adjacent vertices
            sigma2 = atan2(dy2, dx2)
            omega = sigma1 - sigma2                             # Vertices inner angle

            if i == 0:
                sigma += sigma2                                 # increase by first edge´s sigma
            sigma += (self.R(omega) * edge_len) / edge_len      # Increase total sigma by edges r value weighted by it´s length

        return self.MBR_FromSigma(bld_copy, sigma)
    
    def WB(self, bld : QPolygonF) -> QPolygonF:
        bld_copy = bld[ : ]
        
        diags = {}                      # diagonals
        n = len(bld_copy)

        for i in range(n):              # compute each unique (direction independent) diagonal
            for j in range(n):
                if ((n > 3) and (i != j) and ((i + 1) % n != j) and ((i - 1) % n != j) and f'{j}_{i}' not in diags.keys())\
                    or ((n == 3) and (i != j) and f'{j}_{i}' not in diags.keys()):      # Replace The diagonal with edges if building is a triangle, compute diagonals if it has > 3 vertices
                    dx, dy, l2_dist = self.coordDiffDist(bld_copy[i], bld_copy[j])
                    diags.update({f'{i}_{j}' : l2_dist})

        in_bld, out_bld = self.innerDiags(bld_copy, diags)                              # Sort diagonals by inside/outside building status    
        bestDiags = []                                                                  # preferred diagonals                       
        in_bld_len = len(in_bld)                                                        # Amount of diagonals inside the building

        if in_bld_len >= 2:                                                             # there are 2 or more diagonals inside the building
            for i in range(2):
                bestDiags.append(in_bld.pop(0))                                         # Use them in further calculations
        elif in_bld_len == 1:                                                           # only 1 diagonal inside the building
            bestDiags.append(in_bld.pop(0))
            bestDiags.append(out_bld.pop(0))
            bestDiags.sort(key = lambda i : i[1], reverse = True)
        else:                                                                           # no diagonals inside the building
            for i in range(2):
                bestDiags.append(out_bld.pop(0))   

        lengths, sigmas = [], []
        for i in range(2):
            lengths.append(bestDiags[i][1])                                             # Best diagonals´ lengths

            diag_pnts = [int(i) for i in bestDiags[i][0].split('_')]
            dx, dy, tmp = self.coordDiffDist(bld_copy[diag_pnts[0]], bld_copy[diag_pnts[1]])
            sigmas.append(atan2(dy, dx))                                                # Best diagonals´ sigmas

        sigma = ((sigmas[0] * lengths[0]) + (sigmas[1] * lengths[1])) / (sum(lengths))  # Buildings´ sigma
        return self.MBR_FromSigma(bld_copy, sigma)

    def LE_Sigma(self, bld : QPolygonF) -> float:
        n = len(bld)                           
        max_len = 0

        for i in range(n):                
            dx, dy, edge_len = self.coordDiffDist(bld[i % n], bld[(i + 1) % n])

            if edge_len > max_len:          # Update the longest edge and it's sigma
                max_len = edge_len
                sigma = atan2(dy, dx)

        return sigma       

    def MBR_FromSigma(self, bld : QPolygonF, sigma : float) -> QPolygonF:
        bld_rot = self.rotate(bld, -sigma)              # Rotate the building by - Sigma
        mmb_rot = self.minMaxBox(bld_rot)               # Find MBR of the rotated building
        mmb_unrot = self.rotate(mmb_rot, sigma)         # Rotate the MBR back to original position
        return self.resizeRect(mmb_unrot, bld)          # Resize the MBR to fit the original building
    
    def innerDiags(self, bld : QPolygonF, diags : dict) -> tuple[list, list]:
        out_bld, to_pop = {}, []
        n = len(bld)

        if n == 3:                                              # return 2 longest edges as diagonals inside buidling if building is a triangle 
            diags = sorted(diags.items(), key = lambda i : i[1], reverse = True)
            out_bld = diags.pop(diags.index(min(diags, key = lambda i : i[1])))
            return diags, out_bld
        else:                                                   # identify diagonals inside and outside building if it has > 3 vertices
            for key in diags.keys():                            # for each diagonal
                diag_pnts = [int(i) for i in key.split('_')]
                p1 = bld[diag_pnts[0]]                          # 1st section = tested diagonal
                p2 = bld[diag_pnts[1]]

                for i in range(n):                              # Compute diagonal-edge intersection for each edge of the building
                    p3 = bld[i]                                 # 2nd section = current edge
                    p4 = bld[(i + 1) % n]

                    u = (p2.x() - p1.x(), p2.y() - p1.y())
                    v = (p4.x() - p3.x(), p4.y() - p3.y())
                    w = (p1.x() - p3.x(), p1.y() - p3.y())

                    k1 = (v[0] * w[1]) - (v[1] * w[0])
                    k3 = (v[1] * u[0]) - (v[0] * u[1])
                    alpha = k1 / k3

                    if not ((alpha < EPS) or ((alpha + EPS) > 1) and ((p1 in (p3, p4)) or (p2 in (p3, p4)))):
                        to_pop.append(key)                      # diagonal not fully inside building - diagonal intersects the edge outside diagonal´s vertices
                        break                                   # skip to next diagonal
                    elif not self.windingNum(bld, QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)):   # test if diagonal´s center is the polygon
                        to_pop.append(key)                      # diagonal´s center not in the polygon
                        break      

            for key in to_pop:                                  # Split diagonals inside/outside the building 
                out_bld[key] = diags.pop(key)
            
        diags = sorted(diags.items(), key = lambda i : i[1], reverse = True)        # Sort diagonals by length in the descending order
        out_bld = sorted(out_bld.items(), key = lambda i : i[1], reverse = True)

        return diags, out_bld

    def windingNum(self, bld: QPolygonF, q: QPointF) -> bool:
        sum = 0                                                                     # Polygon´s winding number
        n = len(bld)                                                                # Number of vertices

        for i in range(n):                                                          # For each point in the polygon
            m0 = bld[(i + 1) % n].x() - bld[i % n].x()                              # Elements of 't' matrix
            m1 = bld[(i + 1) % n].y() - bld[i % n].y()              
            m2 = q.x() - bld[i % n].x()                             
            m3 = q.y() - bld[i % n].y()

            angle = self.get_2line_angle(q, bld[(i) % n], q, bld[(i + 1) % n])      # an angle between tested point and vertices of current edge
            if angle == float('Inf'):                                               # tested point in polygon´s points
                return False
            elif abs(angle - pi) < EPS:                                             # tested point lays on polygon´s edge
                return False

            det = (m0 * m3) - (m1 * m2)                                             # Determinant of 't' matrix
            if det > EPS: 
                plus = True                                                         # Add the angle
            elif det < EPS:
                plus = False                                                        # Subtract the angle

            sum += angle if plus else -angle

        if abs(abs(sum) - (2 * pi)) < EPS:                                          # if sum - 2 * Pi is less than Epsilon, the point lies in the polygon 
            return True
        else:
            return False
        
    def rateAll(self, blds : dict, mbrs : dict, common_k : set) -> tuple[PrettyTable, tuple]:
        pt = PrettyTable(['key', 'delta sigma 1', 'delta sigma 2'])                     # Table with delta sigmas
        d_sig1 = []; d_sig2 = []
        common_k = sorted(common_k)                                                     # Sort keys in ascending order

        for key in common_k:
            sigmas = self.rateSingle(blds[key], mbrs[key])                              # Compute buildings-MBR pairs sigmas
            sigmas_deg = [round(abs((sigma * 180) / np.pi), 2) for sigma in sigmas]     # Convert to degrees, shorten the floating part

            pt.add_row([key, sigmas_deg[0], sigmas_deg[1]])                             # Add id and sigmas to the table
            d_sig1.append(sigmas_deg[0])
            d_sig2.append(sigmas_deg[1])

        mean_d_sig1 = round(np.mean(d_sig1), 2)                                         # sigma1 mean
        mean_d_sig2 = round(np.mean(d_sig2), 2)                                         # sigma2 mean
        s1_ratio = round((self.fineCount(d_sig1) / len(d_sig1)) * 100, 2)               # |sigma1| < 10° ratio
        s2_ratio = round((self.fineCount(d_sig2) / len(d_sig2)) * 100, 2)               # |sigma2| < 10° ratio

        both_count = 0                                                                  # count |sigma1| < 10° & |sigma2| < 10° ratio
        for i in range(len(d_sig2)):
            if (d_sig1[i] < 10) and (d_sig2[i] < 10):
                both_count += 1
        both_ratio = round((both_count / len(d_sig2)) * 100, 2)

        return pt, (mean_d_sig1, mean_d_sig2, s1_ratio, s2_ratio, both_ratio)           # the table and the summary statistics

    def rateSingle(self, bld : QPolygonF, mbr : QPolygonF) -> tuple[float, float]: 
        sigma = self.LE_Sigma(mbr)
        R = self.R(sigma)                   # compute constant used in calculation of sigmas of given building-MBR pair
        sum = 0                             # sum of Ri - R
        sum_sqr = 0                         # squared sum of Ri - R
        m = len(bld)

        for i in range(m):
            dx, dy, tmp = self.coordDiffDist(bld[i % m], bld[(i + 1) % m])
            ri_minus_R = self.R(atan2(dy, dx)) - R

            sum += ri_minus_R               # building-MBR sigma1 sum
            sum_sqr += ri_minus_R ** 2      # building-MBR sigma2 sum

        return (sum * np.pi) / (2 * m), ((sum_sqr ** 1/2) * np.pi) / (2 * m)       # delta sigma1, delta sigma2

    def R(self, sig : float) -> float:
        k = (2 * sig) / np.pi                   # compute k                 
        return ((k - floor(k)) * np.pi) / 2     # compute r from k
    
    def fineCount(self, values : list) -> int:
        count = 0
        for i in range(len(values)):
            if values[i] < 10:
                count += 1      
        return count

    def grahamScan(self, bld : QPolygonF) -> QPolygonF:
        bld_copy = bld[:]      
        bld_copy = self.starShapedPolygon(bld_copy)

        ch = [bld_copy[0], bld_copy[1]]     # Initial convex hull
        j = 2                               # convex hull's length
        n = len(bld_copy)

        try:
            while j < n:                    # until all star shaped polygon´s points get processed
                if self.halfPlaneTest(ch[-2], ch[-1], bld_copy[j]) < -EPS:
                    ch.append(bld_copy[j])  # append point to convex hull if it lies to the left to the line: 
                    j += 1      
                else:
                    ch.pop()                # remove convex hull´s last point if it doesn't
        except IndexError:
            raise FrameworkError
        
        return QPolygonF(ch)                                                     

    def get_2line_angle(self, p_from : QPointF, p_to : QPointF, p_from1 : QPointF, p_to1: QPointF) -> float:
        ux = p_to.x() - p_from.x()                  # create line vector from p1 to p2
        uy = p_to.y() - p_from.y()

        vx = p_to1.x() - p_from1.x()                # create line vector from p1 to p2
        vy = p_to1.y() - p_from1.y()

        dot = ux * vx + uy * vy                     # dot product
        nu = (ux ** 2 + uy ** 2) ** 1/2             # vector norms
        nv = (vx ** 2 + vy ** 2) ** 1/2

        return min(max(dot / (nu * nv), -1), 1)     # Prevents occurrence of values out of range <-1; 1>
    
    def starShapedPolygon(self, bld: QPolygonF) -> QPolygonF:
        s = min(bld, key = lambda k: k.x())                
        q = min(bld, key = lambda k: k.y())                 # find pivot
        x = QPointF(s.x(), q.y())                           # create temporary point for angle calculation

        while x in bld:                                     # Keep moving X the left by 1 pixel until it stops matching a point in input building
            x.setX(x.x() - 1)

        angles = dict()
        n = len(bld)

        for i in range(n):
            if bld[i] != q:
                angles[i] = self.get_2line_angle(q, x, q, bld[i])       # compute an angle (x, q, p_i)

        angles = {key : val for key, val in sorted(angles.items(), key = lambda i : i[1])}      # sort by angle in ascending order

        to_pop = []
        k, v = [key for key in angles.keys()], [val for val in angles.values()]
        n = len(k)

        for i in range(n):
            pnt = bld[k[i]]
            pnt1 = bld[(k[i] + 1) % n]

            if v[i] == v[(i + 1) % n]:                      # if angles equal
                pnt_to_q = (((pnt.x() - q.x()) ** 2) + ((pnt.y() - q.y()) ** 2)) ** 0.5             # pnt to q distance
                pnt1_to_q = (((pnt1.x() - q.x()) ** 2) + ((pnt1.y() - q.y()) ** 2)) ** 0.5          # pnt1 to q distance

                if pnt_to_q < pnt1_to_q:                    # select the closer point if adjacent points have the same angle
                    to_pop.append(k[i])
                else:
                    to_pop.append((k[i] + 1) % n)

        if to_pop:                                          # remove selected points
            tmp = list(bld)
            for i in reversed(to_pop):
                tmp.pop(i)
            bld = QPolygonF(tmp)

        return bld
    
    def rotate(self, mmb : QPolygonF | tuple, sig : float) -> QPolygonF:
        tmp_mmb = self.setInputPol(mmb)
            
        polr = QPolygonF()
        for p in tmp_mmb:                                   # process all points
            xr = p.x() * cos(sig) - p.y() * sin(sig)        # rotate point
            yr = p.x() * sin(sig) + p.y() * cos(sig)

            pr = QPointF(xr, yr)                            # create rotated point
            polr.append(pr)  

        return polr 
    
    def getArea(self, bld : QPolygonF | tuple) -> float:
        tmp_bld = self.setInputPol(bld)

        area = 0                            # polygon area
        n = len(tmp_bld)                    

        for i in range(1, n + 1):           # process all vertices
            area += tmp_bld[i % n].x() * (tmp_bld[(i + 1) % n].y() - tmp_bld[(i - 1) % n].y())

        return abs(area) / 2
    
    def setInputPol(self, pol : QPolygonF | tuple) -> QPolygonF:
        if type(pol) == tuple:     # minmaxbox tuple input
            return QPolygonF([QPointF(pol[1], pol[3]), QPointF(pol[1], pol[2]), QPointF(pol[0], pol[2]), QPointF(pol[0], pol[3])])           
        return pol
   
    def resizeRect(self, mmb: QPolygonF, build: QPolygonF) -> QPolygonF:               
        A_build = self.getArea(build)                                       # compute area of polygons
        A = self.getArea(mmb)

        k = A_build / A

        tx = (mmb[0].x() + mmb[1].x() + mmb[2].x() + mmb[3].x()) / 4        # center of mass
        ty = (mmb[0].y() + mmb[1].y() + mmb[2].y() + mmb[3].y()) / 4

        u1x = mmb[0].x() - tx                                               # vectors from center of mass to rectangle´s vertices 
        u1y = mmb[0].y() - ty

        u2x = mmb[1].x() - tx
        u2y = mmb[1].y() - ty

        u3x = mmb[2].x() - tx
        u3y = mmb[2].y() - ty

        u4x = mmb[3].x() - tx
        u4y = mmb[3].y() - ty


        v1x = tx + sqrt(k) * u1x                                            # new vertices
        v1y = ty + sqrt(k) * u1y

        v2x = tx + sqrt(k) * u2x
        v2y = ty + sqrt(k) * u2y

        v3x = tx + sqrt(k) * u3x
        v3y = ty + sqrt(k) * u3y

        v4x = tx + sqrt(k) * u4x
        v4y = ty + sqrt(k) * u4y

        v1 = QPointF(v1x, v1y)
        v2 = QPointF(v2x, v2y)
        v3 = QPointF(v3x, v3y)
        v4 = QPointF(v4x, v4y)

        return QPolygonF([v1, v2, v3, v4])                                  # return resized polygon
    
    def setCCW_Orientation(self, blds : dict) -> dict:
        for key, bld in blds.items():
            sum = 0
            n = len(bld)                                    # Amount of vertices

            for i in range(1, n + 1):                       # Test each vertex
                sum += bld[i % n].x() * (bld[(i + 1) % n].y() - bld[(i - 1) % n].y())

            if sum > EPS:                                   # Clockwise rotation -> coordinate reversal
                pnts = [pnt for pnt in bld]
                blds[key] = QPolygonF(reversed(pnts))    
        return blds
    
    def removeDupl(self, blds : dict) -> dict:
        for key, bld in blds.items():
            bld_copy = bld[:]                           # physical copy
            n = len(bld_copy)
            unique_pnts = []

            for i in range(n):
                if bld_copy[i] not in unique_pnts:      # Don't append the point to output polygon if it's already there
                    unique_pnts.append(bld_copy[i])
        
            if n != len(unique_pnts):                   # Recreate the Polygon if number of unique vertices differs from input polygon
                blds[key] = QPolygonF(unique_pnts)
        return blds

    def strictC_Hull(self, ch : QPolygonF) -> QPolygonF:
        n = len(ch)
        ch_copy = [pnt for pnt in ch]
        to_pop = []

        for i in range(len(ch_copy)):                   # If points with adjacent order share at least one coordinate
            if (ch_copy[i].x() == ch_copy[(i + 1) % n].x()) or (ch_copy[i].y() == ch_copy[(i + 1) % n].y()):
                to_pop.append(i % n)                    # Select the first of them to be removed
        
        if to_pop:                                      
            for i in reversed(to_pop):
                ch_copy.pop(i)
            
            return QPolygonF(ch_copy)
        return ch
    
    def halfPlaneTest(self, p_from : QPointF, p_to: QPointF, p_test: QPointF) -> float:
        line_x = p_from.x() - p_to.x()          # line vector´s components
        line_y = p_from.y() - p_to.y()

        ux = p_to.x() - p_test.x()              # line´s 2nd point to tested point vector
        uy = p_to.y() - p_test.y()

        return (line_x * uy) - (line_y * ux)    # test´s determinant
    
    def minMaxBox(self, pol: QPolygonF | list) -> tuple:
        x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')    # Values that will be overwritten on first comparison
        try:        
            x = pol[0][1]           # Polygon consists of QPointF data type
            y = pol[0][0]
        except:
            x = pol[0].x()          # Polygon consists of nested lists
            y = pol[0].y()

            x_min = pol[0].x(); y_max = pol[0].x(); y_min = pol[0].y(); y_max = pol[0].y()          # Swap values to compare with pixel coordinates correctly    
    
        for pnt in pol:
            try:        
                x = pnt[1]          # Polygon consists of QPointF data type
                y = pnt[0]
            except:
                x = pnt.x()         # Polygon consists of nested lists
                y = pnt.y()

            if x < x_min:
                x_min = x
            elif x > x_max:
                x_max = x
            
            if y < y_min:
                y_min = y
            elif y > y_max:
                y_max = y

        return x_min, x_max, y_min, y_max   
    
    def coordDiffDist(self, p1 : QPointF, p2 : QPointF) -> tuple[float, float, float]:
        dx = p2.x() - p1.x()                        # coordinate differences
        dy = p2.y() - p1.y()
        l2_dist = (dx ** 2 + dy ** 2) ** 1/2        # euclidean distance

        return dx, dy, l2_dist
    
    def sjtsk2Pixel(self, point : list, width : int, height : int, x_min : float, x_max : float, y_min : float, y_max : float) -> tuple:        
        del_pix_x = width - 10                                          # amount of widget´s horizontal pixels used for data
        del_pix_y = height - 10
        del_data_x = abs(x_max - x_min)                                 # data X-coord delta
        del_data_y = abs(y_max - y_min)
        
        x = 5 + abs((point[0] - y_min) / del_data_y) * del_pix_x        # Point´s new coordinates    
        y = 5 + abs((point[1] - x_max) / del_data_x) * del_pix_y        

        return x, y  
    
    def rescaleAll(self, blds : dict, mbrs : dict, w : int, h : int) -> tuple [dict, dict]:
        x_min = float('Inf'); x_max = float('-Inf'); y_min = float('Inf'); y_max = float('-Inf')        # bouding box´s inicial values
        data = (blds, mbrs)

        for i in range(len(data)):
            for pol in data[i].values():
                box = self.minMaxBox(pol)

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

        for i in range(len(data)):
            for key, pol in data[i].items():
                j = 0
                for pnt in pol:                                     # Update each point´s coordinates
                    x = 5 + (pnt.x() - 5 - x_min) * x_axes_ratio
                    y = 5 + (pnt.y() - 5 - y_min) * y_axes_ratio

                    pol[j] = QPointF(x, y)                          # Save the point into original data type
                    j += 1
                data[i][key] = pol   

        return blds, mbrs                                           # Return the blds with updated min-max box