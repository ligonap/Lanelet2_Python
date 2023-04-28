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
    points_cent   = []
    
    for data in data_list:
        x0 = float(data[0])
        y0 = float(data[1])
        points_list_0.append((x0,y0))
        
        x1 = float(data[2])
        y1 = float(data[3])
        points_list_1.append((x1,y1))

        cent_x = (x0 + x1) / 2
        cent_y = (y0 + y1) / 2
        points_cent.append((cent_x, cent_y))
        
        
    # Make a Lanelet-Object
    lat = 0
    lon = 0

    lanelet_map_ = LaneletMap(lat, lon)
    
    # Save the first point as the last point of the track
    last_point_line0 = lanelet_map_.add_and_get_Point(points_list_0[0][0], points_list_0[0][1])
    last_point_line1 = lanelet_map_.add_and_get_Point(points_list_1[0][0], points_list_1[0][1])
    last_point_cent  = lanelet_map_.add_and_get_Point(points_cent[0][0], points_cent[0][1])

    st_point_line0 = last_point_line0
    st_point_line1 = last_point_line1
    st_point_cent  = last_point_cent  


    # Make a Lanelet2 Map
    for x in range(1, len(points_list_0)):

        nd_point_line0 = lanelet_map_.add_and_get_Point(points_list_0[x][0], points_list_0[x][1])
        nd_point_line1 = lanelet_map_.add_and_get_Point(points_list_1[x][0], points_list_1[x][1])
        nd_point_cent  = lanelet_map_.add_and_get_Point(points_cent[x][0], points_cent[x][1])
        
        line_0 = lanelet_map_.add_and_get_lineString(st_point_line0, nd_point_line0)
        line_1 = lanelet_map_.add_and_get_lineString(st_point_line1, nd_point_line1)
        cent   = lanelet_map_.add_and_get_lineString(st_point_cent, nd_point_cent)
        
        lanelet_map_.add_Lanelet_with_Centerline(line_0, line_1, cent)
        
        st_point_line0 = nd_point_line0
        st_point_line1 = nd_point_line1
        st_point_cent  = nd_point_cent
        
        # Ring closure
        if x == len(points_list_0)-1:            
            nd_point_line0 = last_point_line0
            nd_point_line1 = last_point_line1
            nd_point_cent  = last_point_cent
            
            line_0 = lanelet_map_.add_and_get_lineString(st_point_line0, nd_point_line0)
            line_1 = lanelet_map_.add_and_get_lineString(st_point_line1, nd_point_line1)
            cent   = lanelet_map_.add_and_get_lineString(st_point_cent, nd_point_cent)
        
            lanelet_map_.add_Lanelet_with_Centerline(line_0, line_1, cent)
        
        
    # Write the Lanelet2 map into a OSM file
    lanelet_map_.write_LaneletMap_to_file("Data_Map_with_centerline.osm")
    
    # what has been loaded?
    lanelet_map_.draw_map()
    
