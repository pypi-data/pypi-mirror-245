from .utils import config


def shape2tess(netiface, params):
    # params:
    # - folder_path
    # - is_use_center_line
    # - is_use_lon_and_lat
    # - laneFileName
    # - laneConnectorFileName
    
    folder_path = params["folder_path"]
    is_use_lon_and_lat = params["is_use_lon_and_lat"]
    is_use_center_line = params["is_use_center_line"]
    laneFileName = params["laneFileName"]
    laneConnectorFileName = params["laneConnectorFileName"]
    
    config.sceneScale = netiface.sceneScale()
    
    from .utils.get_info import get_info
    from .utils.create_road import create_road
    
    # 读取数据
    links_info, connector_info, other_info = get_info(folder_path, is_use_lon_and_lat, is_use_center_line, laneFileName, laneConnectorFileName)

    # import json
    # data = {"link":str(links_info), "connector": str(connector_info)}
    # with open('data.json', 'w') as json_file:
    #     json.dump(data, json_file)

    # 创建路段和连接段
    error_message = create_road(netiface, links_info, connector_info, other_info)

    return error_message





