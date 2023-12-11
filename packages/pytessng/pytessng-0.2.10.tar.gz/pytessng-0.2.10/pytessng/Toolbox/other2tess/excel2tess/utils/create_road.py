from tqdm import tqdm

from .functions import get_coo_list

def create_road(netiface, links_info, connector_info):
    netiface.setNetAttrs("Excel 路网")

    width, height = 600, 400

    error_links = []
    
    # 创建路段
    for link_id in tqdm(links_info):
        link_info = links_info[link_id]
        
        linkName = link_info["linkName"]
        linkCount = link_info["linkCount"]
        linkPoint = get_coo_list(link_info["points"])
        
        # 场景宽度和高度
        width = max(width, max([abs(p[0]) for p in link_info["points"]]))
        height = max(height, max([abs(p[1]) for p in link_info["points"]]))
        
        # 创建路段及车道
        try:
            try:
                link_obj = netiface.createLink(linkPoint, linkCount)
            except:
                link_obj = netiface.createLink3D(linkPoint, linkCount)
        except Exception as e:
            print(str(e))
            error_links.append(link_id)
            continue

        # 判断路段是否存在，并设置属性
        if link_obj:
            link_obj.setName(f"{link_id}-{linkName}")
            links_info[link_id]['obj'] = link_obj
        else:
            error_links.append(link_id)
    
    # 设置场景宽度和高度
    netiface.setSceneSize(width*2+20, height*2+20) # (m)
    
    
    # # 创建连接段
    # for connector_road_tuple, connector_info in tqdm(connector_info.items()):
    #     from_link = links_info[connector_road_tuple[0]]['obj']
    #     to_link = links_info[connector_road_tuple[1]]['obj']
    #
    #     from_link_id, to_link_id = from_link.id(), to_link.id()
    #
    #     from_lane_numbers, to_lane_numbers = [], []
    #     for connector in connector_info:
    #         from_lane_numbers.append(connector['from_lane_number'])
    #         to_lane_numbers.append(connector['to_lane_number'])
    #
    #     netiface.createConnector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)


    error_message = f"路段创建失败的行数：\n{error_links}"

    return error_message
