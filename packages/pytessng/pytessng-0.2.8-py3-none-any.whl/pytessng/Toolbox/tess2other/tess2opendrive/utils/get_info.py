# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 00:12:23 2023

@author: Lenovo
"""

from xml.dom import minidom

from .node import Doc
from .models import Junction, Connector, Road

def get_info(netiface, proj_center:tuple):
    connectors = []
    junctions = []
    for ConnectorArea in netiface.allConnectorArea():
        junction = Junction(ConnectorArea)
        junctions.append(junction)
        for connector in ConnectorArea.allConnector():
            # 为所有的 车道连接创建独立的road，关联至 junction
            for laneConnector in connector.laneConnectors():
                connectors.append(Connector(laneConnector, junction))

    roads = []
    for link in netiface.links():
        roads.append(Road(link))

    # 路网绘制成功后，写入xodr文件
    doc = Doc()
    # 如果有投影中心的信息
    if proj_center[0] and proj_center[1]:
        doc.init_doc(proj_center=proj_center)
    else:
        doc.init_doc()
    doc.add_junction(junctions)
    doc.add_road(roads + connectors)

    uglyxml = doc.doc.toxml()
    xml = minidom.parseString(uglyxml)
    xml_pretty_str = xml.toprettyxml()
    
    return xml_pretty_str