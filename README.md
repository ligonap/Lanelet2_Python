# LaneletMap
A simple Python class for easier handling of Lanelet2 maps.

An existing Lanelet2 map in OSM format can be loaded or created.

As an example, a CSV file (Point_Data_Map.csv) can be read in and saved as an OSM file.
The OSM file can be read in again as a Lanelet2 map at any time.

Point_Data_Map.csv : 56 line each with four (x,y)-points 

CSV_To_Lanelet2_Map.py : Reads a CSV file with four rows of (x,y)-points, shows all LineStrings (four rings) and writes an OSM file. A lanelet consists of two LineStrings of two points each.

CSV_To_Lanelet2_Map_with_centerline.py : Reads in a CSV file with (x,y) points, but shows only two rows of LineStrings (two rings) and one CenterLine and writes an OSM file. A lanelet consists of two LineStrings of two points each and a CenterLine of two points each.

Show_Lanelet2_Map.py : Reads Data_Map.osm, shows the adjacent lanelets to lanelet 1112 and displays the map.
