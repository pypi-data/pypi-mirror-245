from .utils import config


def excel2tess(netiface, params):
    # params:
    # - file_path
    
    file_path = params["file_path"]
    
    config.sceneScale = netiface.sceneScale()
    
    from .utils.get_info import get_info
    from .utils.create_road import create_road
    
    # 读取数据
    links_info, connector_info = get_info(file_path)
    
    # 创建路段和连接段
    error_message = create_road(netiface, links_info, connector_info)

    return error_message

