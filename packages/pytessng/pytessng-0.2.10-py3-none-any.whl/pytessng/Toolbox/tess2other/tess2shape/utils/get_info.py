# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 22:29:53 2023

@author: Lenovo
"""

import collections
from pyproj import Proj
import geopandas as gpd
from shapely.geometry import LineString

from .functions import point2latlon, qtpoint2point

def get_roads_info(links, connectors):
    from .config import lon_0, lat_0

    # 有投影中心经纬度就转为经纬度，否则就用X/Y
    if lon_0 and lat_0:
        projection = Proj(f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84')
        isUseRealLoc = True
    else:
        isUseRealLoc = False

    roads_info = collections.defaultdict(dict)

    for link in links:
        roads_info['links'][link.id()] = {
            'lanes': {}
        }

        action_type = {
            'driving': '机动车道',
            'biking': '非机动车道',
            'sidewalk': '人行道',  # 行人道实际无意义
            'stop': '应急车道',
        }
        action_type = {
            v: k for k, v in action_type.items()
        }
        for lane in link.lanes():
            points = qtpoint2point(lane.centerBreakPoint3Ds())
            if isUseRealLoc:
                points = point2latlon(points, projection)
            roads_info['links'][link.id()]["lanes"][lane.id()] = {
                'points': points,
                'type': action_type[lane.actionType()],
                'number': lane.number() + 1,
                'width': lane.width(),
            }

    for connector in connectors:
        roads_info['connectors'][connector.id()] = {
            "lane_connectors": []
        }

        for lane_connector in connector.laneConnectors():
            points = qtpoint2point(lane_connector.centerBreakPoint3Ds())
            if isUseRealLoc:
                points = point2latlon(points, projection)
            roads_info['connectors'][connector.id()]['lane_connectors'].append(
                {
                    'from_lane_id': lane_connector.fromLane().id(),
                    'to_lane_id': lane_connector.toLane().id(),
                    'points': points,
                }
            )
    
    return roads_info


def get_info(netiface):
    links = netiface.links()
    connectors = netiface.connectors()
    network_json = get_roads_info(links, connectors)

    # 创建路段的 GeoDataFrame
    lane_features = []
    for link_id, link_info in network_json['links'].items():
        for lane_id, lane_info in link_info['lanes'].items():
            feature = {
                'id': lane_id,
                'roadId': link_id,
                'type': lane_info['type'],
                'laneNumber': lane_info['number'],
                'width': lane_info['width'],
                'geometry': LineString(lane_info['points'])
            }
            lane_features.append(feature)
    
    lane_gdf = gpd.GeoDataFrame(lane_features, crs="EPSG:4326")
    
    # 创建连接段的 GeoDataFrame
    if 'connectors' in network_json:
        connector_features = []
        for connector_id, connector_info in network_json['connectors'].items():
            for lane_connector_info in connector_info['lane_connectors']:
                feature = {
                    'preLaneId': lane_connector_info['from_lane_id'],
                    'sucLaneId': lane_connector_info['to_lane_id'],
                    'geometry': LineString(lane_connector_info['points'])
                }
                connector_features.append(feature)
        
        connector_gdf = gpd.GeoDataFrame(connector_features, crs="EPSG:4326")
    else:
        connector_gdf = None
    
    return lane_gdf, connector_gdf