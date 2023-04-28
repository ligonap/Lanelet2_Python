#!/usr/bin/env python

from LaneletMap import LaneletMap

if __name__ == '__main__':
    
    map_source ='Data_Map.osm'
    lat = 0
    lon = 0
    
    lanelet_map_ = LaneletMap(lat, lon, map_source)

    # Lanelets IDs: Neighbor and following
    # 1111 -> 1100 -> 1089 -> 1078
    # 1112 -> 1101 -> 1090 -> 1079
    # 1113 -> 1102 -> 1091 -> 1080
    lane = lanelet_map_.get_Lanelet_with_Id(1112)
    
    print("Current sector:")
    if lanelet_map_.get_leftBound_Lanelet(lane) != None:
        print(lanelet_map_.get_leftBound_Lanelet(lane).id)
    print(lane.id)
    if lanelet_map_.get_rightBound_Lanelet(lane) != None:
        print(lanelet_map_.get_rightBound_Lanelet(lane).id)
    
    print("Next sector:")
    following_lane = lanelet_map_.get_following_Lanelet(lane)
    if lanelet_map_.get_leftBound_Lanelet(following_lane) != None:
        print(lanelet_map_.get_leftBound_Lanelet(following_lane).id)
    print(following_lane.id)
    if lanelet_map_.get_rightBound_Lanelet(following_lane) != None:
        print(lanelet_map_.get_rightBound_Lanelet(following_lane).id)
        
   
    # what has been loaded?
    lanelet_map_.draw_map()
