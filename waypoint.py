from shapely.geometry import Polygon, Point, MultiPolygon, LineString
from shapely import intersection, intersection_all, difference, union_all, union
from shapely.ops import polygonize, unary_union
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PlotPolygon
from matplotlib.patches import Rectangle
from random import random, randrange
from math import comb, dist
from itertools import combinations
import copy
import time



## Class Definition
class Region:
    def __init__(self, poly:Polygon):
        self.poly = poly
        self.x = poly.centroid.x
        self.y = poly.centroid.y
        self.center = (self.x, self.y)
        self.area = poly.area
        self.member_plate = []

    def __str__(self):
        return f"Region Center: {self.center}"
    
class Plate:
    def __init__(self, x=0, y=0, radius=1, id=0):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.center = (x,y)
        self.polygon = Circle(x,y,radius)
        self.intersect_regions = []

    def __str__(self):
        return f"Plate ID: {self.id}, center: {self.center}"
    
    ## Make circle function as polygon
def Circle(x, y, radius):
    return Point(x,y).buffer(radius)

## create list of Plate from coordinates
def CreatePlateScene(coords): # coords is list of (x,y) of plate, e.g. [(1,2),(2,4),(5,1)]
    plates = []
    for (i, plate) in enumerate(coords):
        plates.append(Plate(plate[0],plate[1],1, i))

    return plates

## Print the IDs of Plates in a list
def printID(objects : list):
    for object in objects:
        print(object.id, end=", ")


## Visualisation Functions

def randomColor():
    r = random()
    g = random()
    b = random()
    return (r,g,b)

def visualiseScene(regions = [], waypoints = [], show_wp_radius = True, plates = [], show_plate_radius = False, show_table = False, show_table_buffer = True, tables = [Polygon(((-1,-0.5),(-1, 0.5),(1, 0.5),(1,-0.5)))], xlim = [-3,3], ylim = [-2,2]):
    colors = []
    x_range = xlim[1] - xlim[0] 
    y_range = ylim[1] - ylim[0]
    fig, ax = plt.subplots(figsize = (x_range, y_range ))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    # ax.set_title('Shapely Polygons Visualization')
    ax.set_title('')
       
    # Draw Rectangle (Table)
    if show_table:
        all_table = unary_union(tables)
        if show_table_buffer:
            if type(all_table) == MultiPolygon:
                for table in unary_union(tables).geoms:
                    ax.add_patch(PlotPolygon(xy=table.buffer(0.3).exterior.coords, edgecolor='black', facecolor='white', alpha = 1))
            else:
                ax.add_patch(PlotPolygon(xy=all_table.buffer(0.3).exterior.coords, edgecolor='black', facecolor='white', alpha = 1))

        for (i, table) in enumerate(tables):
            ax.add_patch(PlotPolygon(xy=table.exterior.coords, edgecolor='black', facecolor='white', alpha = 1))

    # Draw polygons
    for polygon in regions:
        if not polygon.is_empty:
        # color
            ax.add_patch(PlotPolygon(xy=polygon.exterior.coords, edgecolor='black', facecolor=randomColor(), alpha = 0.5))
    
    # Draw points
    for point in waypoints:
        plt.scatter(point[0],point[1], color ="black", marker='x')
        if show_wp_radius:
            circle = Circle(point[0], point[1], 1)
            ax.add_patch(PlotPolygon(xy=circle.exterior.coords, edgecolor='black', facecolor='black', alpha = 0.2))            
        
    # Draw poitnts for plates
    for point in plates:
        plt.scatter(point[0],point[1], color ="black") ## initially grey
        if show_plate_radius:
            circle = Circle(point[0], point[1], 1)
            ax.add_patch(PlotPolygon(xy=circle.exterior.coords, edgecolor='black', facecolor='black', alpha = 0.1))            
        

    plt.show()

## Original function definition --> too inefficient
# def getIntersectRegions(polygons): ## polygons is the list of all polygon
#     return_list = []
#     for iteration in range (len (polygons)):
#         temp_return_list = return_list
#         combo_list = list(combinations(polygons, len(polygons)-iteration))
#         for (i,combo) in enumerate(combo_list):
#             temp = intersection_all(combo)
#             if not temp.is_empty:
#                 temp = difference(temp, union_all(temp_return_list, grid_size = 0.005), grid_size = 0.009)
#             if not temp.is_empty:
#                 if type(temp) == MultiPolygon:
#                     area_list = [poly.area for poly in temp.geoms]
#                     temp = temp.geoms[area_list.index(max(area_list))]       
#                 return_list.append(temp)

#     return return_list


def getIntersectRegions(polygons): #O(n^2 or higher, depend on polygons)
    
    poly_list = [intersection(a,b) for a, b in combinations(polygons, 2)]   ## combination is O(n^2), intersection complexity varies depending on 
                                                                            ## polygons properties, such as number of vertices, spatial distribution of vertices, geometric relations 
    rings = [LineString(list(poly.exterior.coords)) for poly in poly_list]  
    return_list = [geom for geom in polygonize(unary_union(rings))]         ## O(k) where k is the number of vertices 
    union_poly = unary_union(return_list)
    for polygon in polygons:
        temp = difference(polygon, union_poly)
        if type(temp) == MultiPolygon:
            area_list = [poly.area for poly in temp.geoms]
            temp = temp.geoms[area_list.index(max(area_list))]       
        
        return_list.append(temp)

    return return_list


def ExcludeTableRegion(regions, tables = [Polygon(((-1,-0.5),(-1, 0.5),(1, 0.5),(1,-0.5)))] ):
    results = []
    for region in regions:
        if len(tables) > 1:
            table  = unary_union(tables)
        else:
            table = tables[0]

        result = difference(region, table.buffer(0.3))
        if not result.is_empty:
            if type(result) == MultiPolygon:
                for poly in result.geoms:
                    results.append(poly)
            else:
                results.append(result)
    return results


def LinkRegionAndPlate(regions: list , Plates:list): # Plates is a list of Plates, while regions are polygons    
    Regions = []
    for region in regions:
        r = Region(region)
        for plate in Plates:
            if dist(r.center, plate.center) <=1:
                r.member_plate.append(plate)
                plate.intersect_regions.append(r)
        Regions.append(r)
        
    return Regions

## Start main process loop functions

def getNearestPlate(point, plates):
    
    for (i, plate) in enumerate(plates):
        if i == 0:
            nearest = plate
            nearest_dist = dist(plate.center, point)
        else:
            distance = dist(plate.center, point)
            if distance < nearest_dist:
                nearest = plate
                nearest_dist = distance
                
    return nearest, nearest_dist

def getBestRegion(plate:Plate):
    n = 0
    for (i, region) in enumerate(plate.intersect_regions):
        if i == n:
            if region.area < 0.01:
                n+=1
                continue
            max_plate_region = region
            max_plate_qty = len(region.member_plate)
            
        else:
            plate_qty = len(region.member_plate)
            if plate_qty > max_plate_qty  and region.area >= 0.01:
                max_plate_region = region
                max_plate_qty = len(region.member_plate) 
    
    return copy.deepcopy(max_plate_region), max_plate_qty, max_plate_region.area

def updateRegions(regions, plates):

    plate_ids = [plate.id for plate in plates]

    for region in regions:

        for mem_plate in [i for i in region.member_plate]:

            if mem_plate.id in plate_ids:

                region.member_plate.remove(mem_plate)