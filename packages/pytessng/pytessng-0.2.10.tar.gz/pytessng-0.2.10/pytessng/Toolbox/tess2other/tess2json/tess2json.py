import json
from .utils import config


def tess2json(netiface, params):
    # params:
    # - file_path
    # - lon_0
    # - lat_0
    
    # 文件保存路径
    file_path = params["file_path"]
    
    # 场景比例尺
    config.sceneScale = netiface.sceneScale()
    # 投影中心经纬度
    config.lon_0 = params["lon_0"]
    config.lat_0 = params["lat_0"]
    
    # 导入计算模块
    from .utils.get_info import get_info
    
    # 获取数据
    json_info = get_info(netiface)
    
    # 写入数据
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_info, json_file, indent=4, ensure_ascii=False)