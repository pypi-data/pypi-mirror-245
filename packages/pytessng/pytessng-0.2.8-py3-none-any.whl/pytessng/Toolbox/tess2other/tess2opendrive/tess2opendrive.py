# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 13:40:53 2023

@author: Lenovo
"""

from .utils import config


def tess2opendrive(netiface, params):
    # params:
    # - file_path
    # - lon_0
    # - lat_0
    
    # 文件保存路径
    file_path = params["file_path"]
    lon_0 = params["lon_0"]
    lat_0 = params["lat_0"]
    
    # 场景比例尺
    config.sceneScale = netiface.sceneScale()
    
    # 导入计算模块
    from .utils.get_info import get_info
    
    # 获取数据
    xml_pretty_str = get_info(netiface, (lon_0, lat_0))
    
    # 写入数据
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_pretty_str)