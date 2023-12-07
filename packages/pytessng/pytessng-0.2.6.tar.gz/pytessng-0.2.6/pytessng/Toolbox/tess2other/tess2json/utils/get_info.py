from shapely.geometry import Polygon
from pyproj import Proj

from .functions import p2m, qtpoint2point, calculate_angle_with_y_axis
from tqdm import tqdm

def get_info(netiface):
    data = {
        "name": "",
        "road": [],
        "connector": [],
        "area": [],
        "crosswalk": [],
    }

    from .config import lon_0, lat_0

    # 如果有经纬度信息
    if lon_0 is not None and lat_0 is not None:
        data["header"] = f'+proj=tmerc +lat_0={lat_0} +lon_0={lon_0} +k=1 +ellps=WGS84 +units=m +no_defs'
        projection = Proj(data["header"])
        isHaveRealLoc = True
    else:
        data["header"] = ""
        isHaveRealLoc = False

    # data["header"] = "+proj=tmerc +lat_0=0 +lon_0=114 +k=1 +x_0=500000 +y_0=0 +ellps=GRS80 +units=m +no_defs"
    # projection = Proj(data["header"])
    # isHaveRealLoc = True

    turnType_mapping = {}

    # 保存面域信息
    areas = netiface.allConnectorArea()
    for area in tqdm(areas):
        area_data = {
            "id": area.id(),
            "incommingRoads": [],
            "outgoingRoads": [],
            "connector": [],
            "crosswalk": []
        }

        area_boundary_points = []
        
        # 保存连接段信息
        for connector in area.allConnector():
            connector_data = {
                'id': connector.id(),
                'areaId': area.id(),
                'predecessor': connector.fromLink().id(),
                'successor': connector.toLink().id(),
                'links': []
            }
            
            area_data["connector"].append(connector_data['id'])
            if connector_data['predecessor'] not in area_data["incommingRoads"]:
                area_data["incommingRoads"].append(connector_data['predecessor'])
            if connector_data['successor'] not in area_data["outgoingRoads"]:
                area_data["outgoingRoads"].append(connector_data['successor'])
            
            # 连接段分车道
            for lane_connector in connector.laneConnectors():
                link_data = {
                    'predecessor': lane_connector.fromLane().id(),
                    'successor': lane_connector.toLane().id(),
                    'center_points_tess': qtpoint2point(lane_connector.centerBreakPoint3Ds(), "tess"),
                    'left_points_tess': qtpoint2point(lane_connector.leftBreakPoint3Ds(), "tess"),
                    'right_points_tess': qtpoint2point(lane_connector.rightBreakPoint3Ds(), "tess"),
                }
                link_data['start_points_tess'] = link_data['center_points_tess'][0]
                link_data['end_points_tess'] = link_data['center_points_tess'][-1]
                if isHaveRealLoc:
                    link_data['center_points_real'] = qtpoint2point(lane_connector.centerBreakPoint3Ds(), "real", projection)
                    link_data['left_points_real'] = qtpoint2point(lane_connector.leftBreakPoint3Ds(), "real", projection)
                    link_data['right_points_real'] = qtpoint2point(lane_connector.rightBreakPoint3Ds(), "real", projection)
                    link_data['start_points_real'] = link_data['center_points_real'][0]
                    link_data['end_points_real'] = link_data['center_points_real'][-1]
                link_data['length'] = p2m(lane_connector.length())
                
                connector_data['links'].append(link_data)
                
                start_angle = calculate_angle_with_y_axis(link_data['center_points_tess'][0], link_data['center_points_tess'][1])
                end_angle = calculate_angle_with_y_axis(link_data['center_points_tess'][-2], link_data['center_points_tess'][-1])
                angle_diff = (end_angle - start_angle + 180) % 360 - 180
                if -45 < angle_diff < 45:
                    turnType = "直行"
                elif -135 < angle_diff < -45:
                    turnType = "左转"
                elif 45 < angle_diff < 135:
                    turnType = "右转"
                else:
                    turnType = "掉头"

                if link_data['predecessor'] not in turnType_mapping.keys():
                    turnType_mapping[link_data['predecessor']] = []
                turnType_mapping[link_data['predecessor']].append(turnType)
                
                left_points = qtpoint2point(lane_connector.leftBreakPoint3Ds(), "tess")
                right_points = qtpoint2point(lane_connector.rightBreakPoint3Ds(), "tess")
                one_lane_points = left_points + right_points[::-1]
                x, y, z = zip(*one_lane_points)
                one_lane_points = list(zip(x, y))
                area_boundary_points.append(one_lane_points)
            
            data['connector'].append(connector_data)
            
        try:
            # 构建多边形对象列表
            polygon_list = [Polygon(coords) for coords in area_boundary_points]
            # 计算多边形的并集
            union_polygon = polygon_list[0]
            for polygon in polygon_list[1:]:
                union_polygon = union_polygon.union(polygon)
            # 提取边界点
            union_boundary_coords = list(union_polygon.exterior.coords)
            
            area_data["points_tess"] = union_boundary_coords
            if isHaveRealLoc:
                area_data["points_real"] = [projection(x, y, inverse=True) for x, y in union_boundary_coords]
            
        except:
            pass
        
        data["area"].append(area_data)
    
    
    # 保存路段信息
    for link in tqdm(netiface.links()):
        link_data = {}
        link_data["id"] = link.id()
        link_data['points_tess'] = qtpoint2point(link.centerBreakPoint3Ds(), "tess")
        if isHaveRealLoc:
            link_data['points_real'] = qtpoint2point(link.centerBreakPoint3Ds(), "real", projection)
        link_data['bearing'] = calculate_angle_with_y_axis(link_data['points_tess'][-2], link_data['points_tess'][-1])
        link_data['lanes'] = []
        # 路段分车道
        for lane in link.lanes():
            lane_data = {
                'id': lane.id(),
                'type': lane.actionType(),
                'center_points_tess': qtpoint2point(lane.centerBreakPoint3Ds(), "tess"),
                'left_points_tess': qtpoint2point(lane.leftBreakPoint3Ds(), "tess"),
                'right_points_tess': qtpoint2point(lane.rightBreakPoint3Ds(), "tess")
            }
            lane_data['start_points_tess'] = lane_data['center_points_tess'][0]
            lane_data['end_points_tess'] = lane_data['center_points_tess'][-1]

            if isHaveRealLoc:
                lane_data['center_points_real'] = qtpoint2point(lane.centerBreakPoint3Ds(), "real", projection)
                lane_data['left_points_real'] = qtpoint2point(lane.leftBreakPoint3Ds(), "real", projection)
                lane_data['right_points_real'] = qtpoint2point(lane.rightBreakPoint3Ds(), "real", projection)
                lane_data['start_points_real'] = lane_data['center_points_real'][0]
                lane_data['end_points_real'] = lane_data['center_points_real'][-1]
            lane_data['length'] = p2m(lane.length())
            lane_data['turnType'] = list(set(turnType_mapping.get(lane.id(), [])))
            lane_data['limitSpeed'] = p2m(link.limitSpeed()) # km/h
            
            link_data['lanes'].append(lane_data)
        
        data['road'].append(link_data)
    
    return data

