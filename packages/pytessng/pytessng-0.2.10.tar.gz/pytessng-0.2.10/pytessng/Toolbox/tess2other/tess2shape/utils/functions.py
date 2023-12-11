# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 22:21:18 2023

@author: Lenovo
"""


from PySide2.QtGui import QVector3D

from .config import sceneScale


def p2m(x):
    return x * sceneScale


def qtpoint2point(qtpoints):
    points = []
    for qtpoint in qtpoints:
        points.append(
            (p2m(qtpoint.x()), - p2m(qtpoint.y()), 0) if isinstance(qtpoint, QVector3D) else qtpoint
        )
    return points


# 坐标转经纬度
def point2latlon(points, p):
    new_points = []
    for point in points:
        lon, lat = p(point[0], point[1], inverse=True)
        new_points.append([lon, lat, point[2]])
    # 返回经纬度坐标及z坐标列表
    return new_points


