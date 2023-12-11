import numpy as np
from PySide2.QtGui import QVector3D

from .config import sceneScale


def p2m(x):
    return x * sceneScale

def qtpoint2point(qtpoints):
    x_move = 0
    y_move = 0
    points = []
    for qt_point in qtpoints:
        x = p2m(qt_point.x())
        y = -p2m(qt_point.y())
        z = p2m(qt_point.z())
        x += x_move
        y += y_move
        points.append([x, y, z])
    return points

# 计算向量2相对向量1的旋转角度（-pi~pi）
def clockwise_angle(v1, v2):
    x1, y1 = v1.x, v1.y
    x2, y2 = v2.x, v2.y
    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2
    theta = np.arctan2(det, dot)
    return theta