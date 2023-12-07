import json

from .utils import config


def tess2unity(netiface, params):
    # params:
    # - file_path
    
    # 文件保存路径
    file_path = params["file_path"]
    
    # 场景比例尺
    config.sceneScale = netiface.sceneScale()
    
    # 导入计算模块
    from .utils.get_info import get_info

    # 获取数据
    unity_info = get_info(netiface)

    # 写入数据
    with open(file_path, "w") as json_file:
        json.dump(unity_info, json_file, indent=4)
