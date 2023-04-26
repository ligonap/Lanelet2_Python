#!/usr/bin/env python

import os
import lanelet2
import lanelet2.core as lncore
from lanelet2.core import (BasicPoint2d, GPSPoint, LineString3d, Point3d, getId, Lanelet)
from lanelet2.geometry import (distance, intersects2d, boundingBox2d, to2D)
import matplotlib.pyplot as plt

# A class that allows you to handle a Lanelet2 map with Python.

# Up to four arguments are possible:
# a) LaneletMap()
# b) LaneletMap(latitude)
# c) LaneletMap(latitude, longitude)
# d) LaneletMap(latitude, longitude, osm_map_file)

class LaneletMap:
    def __init__(self, lat = 0.0, lon = 0.0, osm_map_file = "none"):
        
        # file name of the OSM map e.g. <name.osm>
        self.osm_map_file = osm_map_file
        
        # Search latitude and longitude for Lanelets2 map
        self.lat = lat
        self.lon = lon
        
        # Lanelet2 map
        self.lmap = None
        
        # Routing graph ( later e.g. with set_graph() )
        self.graph = None
        
        if not self.osm_map_file == "none":
            """ Initialize LaneletMap from a osm_map_file """
            # Lanelet2 map
            self.lmap = self.load_osm_file_to_lanelet2(self.osm_map_file, self.lat, self.lon)
        
            # Routing graph
            self.graph = self.get_graph()
            
        else:
            """ Initialize LaneletMap without a osm_map_file """
            # Lanelet2 map
            self.lmap = lncore.LaneletMap()



    # Add and get a new Point for the Lanelet2 Map
    # @param x: x coordinate of the Point (float)
    # @param y: y coordinate of the Point (float)
    # @return: A new Point of the Lanelet2 Map
    def add_and_get_Point(self, x: float, y: float):
    
        # add a new Point
        point = Point3d(getId(), x, y, 0)
        self.lmap.add(point)
        
        return point
        
    
    # Add and get a new LineString (first -> second) for the Lanelet2 Map. 
    # @param first_point: first Point from a Line
    # @param second_point: second Point from a Line
    # @return: A new LineString of the Lanelet2 Map
    def add_and_get_lineString(self, first_point, second_point):

        # add a new LineString
        lineString = LineString3d(getId(), [first_point, second_point])
        self.lmap.add(lineString)

        return lineString
        
        
    # Add a new Lanelet to the Lanelet2 Map
    # @param line_left: left LineString of a Lanelet
    # @param line_right: right LineString of a Lanelet
    def add_Lanelet(self, line_left, line_right):

        new_lanelet = Lanelet(getId(), line_left, line_right)

        # add attributes to the Lanelet
        new_lanelet.attributes["location"] = "nonurban"
        new_lanelet.attributes["one_way"] = "yes"
        new_lanelet.attributes["region"] = "de"
        new_lanelet.attributes["subtype"] = "highway"
        
        self.lmap.add(new_lanelet)
    
    
    # Add a new Lanelet to the Lanelet2 Map with a define Centerline
    # @param line_left: left LineString of a Lanelet
    # @param line_right: right LineString of a Lanelet
    # @param centerline: a define Centerline of a Lanelet
    def add_Lanelet_with_Centerline(self, line_left, line_right, centerline):
    
        new_lanelet = Lanelet(getId(), line_left, line_right)
        new_lanelet.centerline = centerline
        
        # add attributes to the Lanelet
        new_lanelet.attributes["location"] = "nonurban"
        new_lanelet.attributes["one_way"] = "yes"
        new_lanelet.attributes["region"] = "de"
        new_lanelet.attributes["subtype"] = "highway"
        
        self.lmap.add(new_lanelet)
        
  
    # load an osm file to a lanelete map
    # @param osm_map_file : Path of a OSM map (String)
    # @param lat : center latitude (float)
    # @param lon : center longitude (float)
    # @return: Lanelet2-Map
    def load_osm_file_to_lanelet2(self, osm_map_file: str, lat: float, lon: float):

        # try to open the modified OSM file
        osm_path = os.path.join(os.path.abspath(os.getcwd()), osm_map_file)
        if not os.path.exists(osm_path):
           print("OSM %s not found!" % (osm_path))
           exit()

        print("using OSM: %s" % (osm_path))

        # Make a Lanelet2 map
        projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat, lon))
        lmap, err_list = lanelet2.io.loadRobust(osm_path, projector)
  
        # Report possible errors
        if len(err_list) != 0:
           for err in err_list:
             print(err)
  
        print("%d errors, %d lanes dectected" % (len(err_list), len([l for l in lmap.laneletLayer])))

        return lmap


    # Generates a routing graph from the Lanelet2 map
    # @return: routing graph
    def get_graph(self):
        traffic_rules = lanelet2.traffic_rules.create(lanelet2.traffic_rules.Locations.Germany,
                                                  lanelet2.traffic_rules.Participants.Vehicle)
                                                  
        return lanelet2.routing.RoutingGraph(self.lmap, traffic_rules)


    # Set a routing graph from the Lanelet2 map
    def set_graph(self):
        self.graph = self.get_graph()
    

    # Set a Lanelet2 map    
    # @param lmap : A new Lanelet2 map
    def set_lamp(self, lmap):
        self.lmap = lamp              
      
                    
    # write the lanelet2 map to an osm file
    # @param target_map : Name of the Lanelet2 map to be written as OSM map.
    def write_LaneletMap_to_file(self, target_map = 'target_map.osm'):

        # Current directory
        path = os.path.join(os.path.abspath(os.getcwd()), target_map)
        
        projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(self.lat, self.lon))
        write_err = lanelet2.io.writeRobust(path, self.lmap, projector)
  
        # Report possible errors
        if len(write_err) != 0:
           for err in write_err:
               print(err)
      

    # Draws a local map (in meter) based on the Lanelet data
    def draw_map(self):

        for line in self.lmap.lineStringLayer:
            x = [] 
            y = []
            for point in line:
                x.append(point.x)
                y.append(point.y)
            plt.plot(x,y) 

        plt.show()    


    # Prints infos of the lanelet map
    def infos_about_the_LaneletMap(self):
    
        print("Number of")
        print("Lanelets: %s" % len(self.lmap.laneletLayer))
        print("Areas: %s" % len(self.lmap.areaLayer))
        print("Regulatory elements: %s" % len(self.lmap.regulatoryElementLayer))
        print("Linestrings: %s" % len(self.lmap.lineStringLayer))
        print("Polygons: %s" % len(self.lmap.polygonLayer))
        print("Points: %s" % len(self.lmap.pointLayer))
           

    # Returns a lanelet by an ID
    # @param ID : Id of the Lanelet (int)
    # @return: a Lanelet else None
    def get_Lanelet_with_Id(self, ID: int):
    
        for lane in self.lmap.laneletLayer:
            if lane.id == ID:
                return lane
                
        print("No Lanelet with ID %s found!" % ID)
        return None    
    
    
    # Returns the CenterLine from a Lanelet
    # @param lane : a Lanelet
    # @return: a centerline
    def get_CenterLine_from_LaneLet(self, lane):
    
        if lane == None:
            print("No Lanelet found")
            return None

        return lane.centerline
        
    # Returns the left bounded Line
    # @param lane : a Lanelet
    # @return: the left bounded Line
    def get_Leftbound_from_Lanelet(self, lane):
    
        if lane == None:
            print("No Lanelet found")
            return None
    
        return lane.leftBound
        
        
    # Returns the left bounded Line
    # @param lane : a Lanelet
    # @return: the right bounded Line
    def get_Rightbound_from_Lanelet(self, lane):
    
        if lane == None:
            print("No Lanelet found")
            return None
    
        return lane.rightBound        

        
    # Returns a line with the ID 
    # @param ID : Id of the Line (int)
    # @return: a Line else None
    def get_Line_with_Id(self, ID: int):
    
        for line in self.lmap.lineStringLayer:
            if line.id == ID:
                return line
        
        print("No Line with ID %s found!" % ID)
        return None       
    
    
    # Returns all Points from a Line as list
    # @param line: a Line
    # @return: a list of Points
    def get_PointList_from_Line(self, line):
        points = []
        for point in line:
            points.append(point) 
    
        return points


    # Returns a point as tuple (x,y)
    # @param point: a Point
    # @return: the tuple (x, y) of the Point
    def get_Point_Tuple(point):
        return (point.x, point.y)                      
   
   
    # Returns a point by an ID
    # @param ID : Id of the Point (int)
    # @return: a Point else None
    def get_Point_with_Id(self, ID: int):
    
        for point in self.lmap.pointLayer:
            if point.id == ID:
                return point
                
        print("No point with ID %s found!" % ID)
        return None    

    
    # Returns the Lanelet ID, if a point (lat, lon) is over a Lanelet
    # @param lat: a latitude (float)
    # @param lon: a longitude (float)
    # @return: a Lanelet ID, matching the coordinates
    def point_ll_over_Lanelet(self, lat: float, lon: float):
    
        gpsPoint = GPSPoint(lat, lon)
        projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(self.lat, self.lon))
        
        xyPoint = to2D(projector.forward(gpsPoint))
        nearest_lanelet = lanelet2.geometry.findNearest(self.lmap.laneletLayer, xyPoint, 1)

        # If this lanelet contains the point, return the id of the lanelet, otherwise None
        if lanelet2.geometry.inside(nearest_lanelet[0][1], xyPoint):
            return nearest_lanelet[0][1].id
        else:
            return None
    
    
    # Returns the Lanelet ID, if a point (x, y) is over a Lanelet
    # @param x: a x-value (float)
    # @param y: a y-value (float)
    # @return: a Lanelet ID, matching the coordinates
    def point_xy_over_Lanelet(self, x: float, y: float):
        
        xyPoint = BasicPoint2d(x, y)
        nearest_lanelet = lanelet2.geometry.findNearest(self.lmap.laneletLayer, xyPoint, 1)
        # If this lanelet contains the point, return the id of the lanelet, otherwise None
        if lanelet2.geometry.inside(nearest_lanelet[0][1], xyPoint):
            return nearest_lanelet[0][1].id
        else:
            return None    
      
       
    # Returns the left bounded Lanelet
    # @param lane: a Lanelet
    # @return: a left bounded Lanelet else None
    def get_leftBound_Lanelet(self, lane):
    
        lanelets = self.lmap.laneletLayer.findUsages(lane.leftBound)
        # In the list are the lane and the leftBound one 
        if lane in lanelets:
            lanelets.remove(lane) # remove the reference lanelet from list
        
        if len(lanelets) == 0:
            return None
            
        return lanelets[0]
        
                        
    # Returns the right bounded lanelet
    # @param lane: a Lanelet
    # @return: a right bounded Lanelet else None
    def get_rightBound_Lanelet(self, lane):
    
        lanelets = self.lmap.laneletLayer.findUsages(lane.rightBound)
        # In the list are the lane and the rightBound one 
        if lane in lanelets:
            lanelets.remove(lane) # remove the reference lanelet from list
        
        if len(lanelets) == 0:
            return None
                
        return lanelets[0]
        
        
    # Return the directly following Lanlet
    # @param lane: a Lanelet
    # @return: a following Lanelet    
    def get_following_Lanelet(self, lane):
    
        if self.graph == None:
            self.graph = self.get_graph()
               
        following_Lanelet_id = (self.graph.following(lane))[0].id
        
        return self.get_Lanelet_with_Id(following_Lanelet_id)

