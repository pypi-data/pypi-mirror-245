import os
import collections
import pandas as pd

###############################################################################


# 获取路段信息
def get_links_info(file_path):
    _, extension = os.path.splitext(file_path)
    # 读取文件
    if extension == ".csv":
        data = pd.read_csv(file_path)
    elif extension in [".xlsx", ".xls"]:
        data = pd.read_excel(file_path)
    else:
        raise Exception("Invaild file format !")
    ID = 2
    # 保存路段信息
    links_info = collections.defaultdict(dict)
    for col in data.to_numpy():
        links_info[ID]["linkName"] = col[0] if col[0] else ID
        links_info[ID]["linkCount"] = int(col[1])
        links_info[ID]["points"] = [list(map(int, j.split(","))) for j in col[2:] if str(j)!="nan"]
        ID += 1
    
    return links_info


def get_info(file_path):
    # 读取路段数据
    links_info = get_links_info(file_path)
    connector_info = {}
    
    return links_info, connector_info