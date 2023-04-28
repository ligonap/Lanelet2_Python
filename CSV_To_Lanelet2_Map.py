#!/usr/bin/env python

import csv
from LaneletMap import LaneletMap

if __name__ == '__main__':

    source_name = "Point_Data_Map.csv"

    # Open a file
    try:
        csvfile = open(source_name, "r+")
        print ("Source file name: ", csvfile.name)
        
    except IOError:
        print ("There was an error reading to", source_name)
        sys.exit()  

    # Transfer the csv data to a list
    csvReader = csv.reader(csvfile, delimiter = ',')
    data_list = []
    data_list.extend(csvReader)

    # Close opened file
    csvfile.close()

    # Extract the data from the csv into four point lists
    points_list_0 = []
    points_list_1 = []
    points_list_2 = []
    points_list_3 = []

    for data in data_list:
        x0 = float(data[0])
        y0 = float(data[1])
        points_list_0.append((x0,y0))
        
        x1 = float(data[2])
        y1 = float(data[3])
        points_list_1.append((x1,y1))
        
        x2 = float(data[4])
        y2 = float(data[5])
        points_list_2.append((x2,y2))
        
        x3 = float(data[6])
        y3 = float(data[7])
        points_list_3.append((x3,y3))
        
    # Make a Lanelet-Object
    lat = 0
    lon = 0

    lanelet_map_ = LaneletMap(lat, lon)
    
    # Save the first point as the last point of the track
    last_point_line0 = lanelet_map_.add_and_get_Point(points_list_0[0][0], points_list_0[0][1])
    last_point_line1 = lanelet_map_.add_and_get_Point(points_list_1[0][0], points_list_1[0][1])
    last_point_line2 = lanelet_map_.add_and_get_Point(points_list_2[0][0], points_list_2[0][1])
    last_point_line3 = lanelet_map_.add_and_get_Point(points_list_3[0][0], points_list_3[0][1])
    
    st_point_line0 = last_point_line0
    st_point_line1 = last_point_line1
    st_point_line2 = last_point_line2
    st_point_line3 = last_point_line3
    
    
    # Make a Lanelet2 Map
    for x in range(1, len(points_list_0)):

        nd_point_line0 = lanelet_map_.add_and_get_Point(points_list_0[x][0], points_list_0[x][1])
        nd_point_line1 = lanelet_map_.add_and_get_Point(points_list_1[x][0], points_list_1[x][1])
        nd_point_line2 = lanelet_map_.add_and_get_Point(points_list_2[x][0], points_list_2[x][1])
        nd_point_line3 = lanelet_map_.add_and_get_Point(points_list_3[x][0], points_list_3[x][1])
        
        line_0 = lanelet_map_.add_and_get_lineString(st_point_line0, nd_point_line0)
        line_1 = lanelet_map_.add_and_get_lineString(st_point_line1, nd_point_line1)
        line_2 = lanelet_map_.add_and_get_lineString(st_point_line2, nd_point_line2)
        line_3 = lanelet_map_.add_and_get_lineString(st_point_line3, nd_point_line3)
        
        lanelet_map_.add_Lanelet(line_0, line_1)
        lanelet_map_.add_Lanelet(line_1, line_2)
        lanelet_map_.add_Lanelet(line_2, line_3)
        
        st_point_line0 = nd_point_line0
        st_point_line1 = nd_point_line1
        st_point_line2 = nd_point_line2
        st_point_line3 = nd_point_line3
        
        # Ring closure
        if x == len(points_list_0)-1:            
            nd_point_line0 = last_point_line0
            nd_point_line1 = last_point_line1
            nd_point_line2 = last_point_line2
            nd_point_line3 = last_point_line3
            
            line_0 = lanelet_map_.add_and_get_lineString(st_point_line0, nd_point_line0)
            line_1 = lanelet_map_.add_and_get_lineString(st_point_line1, nd_point_line1)
            line_2 = lanelet_map_.add_and_get_lineString(st_point_line2, nd_point_line2)
            line_3 = lanelet_map_.add_and_get_lineString(st_point_line3, nd_point_line3)
        
            lanelet_map_.add_Lanelet(line_0, line_1)
            lanelet_map_.add_Lanelet(line_1, line_2)
            lanelet_map_.add_Lanelet(line_2, line_3)
        
        
    # Write the Lanelet2 map into a OSM file
    lanelet_map_.write_LaneletMap_to_file("Data_Map.osm")
    
    # what has been loaded?
    lanelet_map_.draw_map()
    
