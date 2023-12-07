import os
import shutil
import traceback

from PySide2.QtGui import QVector3D
from PySide2.QtCore import QPointF

from .utils.functions import AdjustNetwork, line2surface, simplify_tessng_file

###############################################################################

def update_sceneScale(netiface):
    from .utils import config
    
    # 场景比例尺
    config.sceneScale = netiface.sceneScale()


# 创建路段
def createLink(netiface, input_info):
    # 更新场景比例尺
    update_sceneScale(netiface)
    from .utils.functions import m2p

    # 如果输入框有信息
    if input_info:
        try:
            point_1_x, point_1_y, point_1_z, point_2_x, point_2_y, point_2_z, *move = [float(i) for i in input_info.split(",")]
            move = move[0] if move else 0
            center_points = line2surface([(point_1_x, point_1_y, point_1_z), (point_2_x, point_2_y, point_2_z)], move)
            qt_center_points = [QVector3D(m2p(point[0]), - m2p(point[1]), m2p(point[2])) for point in center_points]
            netiface.createLink3D(qt_center_points, 3)
            return True, None
        except:
            error = str(traceback.format_exc())
            print(error)
            message = "参数输入错误，请检查！"
            return False, message
    else:
        message = "请参照提示信息输入\n起点横坐标,起点纵坐标,起点Z坐标,终点横坐标,终点纵坐标,终点Z坐标(,整体偏移距离(向右为正))"
        return False, message


# 打断路段
def splitLink(netiface, input_info):
    # 更新场景比例尺
    update_sceneScale(netiface)
    from .utils.functions import m2p

    # 如果输入框有信息
    if input_info:
        try:
            split_infos = input_info.split(";")
            split_distances = []
            for split_info in split_infos:
                link_id, point_x, point_y = split_info.split(",")
                link_id, point_x, point_y = int(link_id), float(point_x), float(point_y)

                # 由于替换了插件，所以要把这句话注释掉
                netiface.buildNetGrid()

                locations = netiface.locateOnCrid(QPointF(m2p(point_x), -m2p(point_y)), 9)
                
                for location in locations:
                    # 因为C++和python调用问题，必须先把lane实例化赋值给
                    if location.pLaneObject.isLane():
                        lane = location.pLaneObject.castToLane()
                        if lane.link().id() == link_id:
                            distance = location.distToStart
                            print("寻找到最近点", link_id, (point_x, point_y), location.point)
                            split_distances.append([link_id, distance])
                            break
            adjust_obj = AdjustNetwork(netiface)
            message = adjust_obj.split_link(split_distances)
            return True, message
        except:
            error = str(traceback.format_exc())
            print(error)
            message = "参数输入错误，请检查！"
            return False, message
    else:
        message = "请参照提示信息输入\n路段ID,断点横坐标,断点纵坐标;\n路段ID,断点横坐标,断点纵坐标...\n每组打断信息以< ; >分隔,内部以< , >分隔"
        return False, message
    

# 连接路段
def joinLink(netiface):
    # 更新场景比例尺
    update_sceneScale(netiface)

    # 如果没有路段
    if not netiface.linkCount():
        message = "当前没有路段！"
        return False, message
    
    adjust_obj = AdjustNetwork(netiface)
    message = adjust_obj.join_link()
    
    return True, message


# 简化路网
def simplifyTessngFile(netiface):
    update_sceneScale(netiface)

    # 获取文件路径
    netFilePath = netiface.netFilePath()
    
    if not netFilePath.endswith(".tess"):
        message = "请打开合适的 tess 路网"
        return False, message
    
    # 将源文件复制再进行操作
    # 获取原文件的目录路径
    file_directory = os.path.dirname(netFilePath)
    # 提取原文件的文件名和扩展名
    file_name, file_extension = os.path.splitext(os.path.basename(netFilePath))
    # 生成新文件的路径
    new_file_path = file_directory + f'\\{file_name}-简化版{file_extension}'
    # 复制文件
    shutil.copy(netFilePath, new_file_path)
    
    try:
        message = simplify_tessng_file(new_file_path)
        netiface.openNetFle(new_file_path)
        return True, message
    except:
        message = "路网简化失败, 请联系开发者"
        return False, message