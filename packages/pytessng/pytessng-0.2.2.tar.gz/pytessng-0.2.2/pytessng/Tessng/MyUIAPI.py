import os
import sys
import traceback
from pathlib import Path
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import QCoreApplication

from DLLs.Tessng import tessngIFace
from Tessng.MyUI import MyUI
from Toolbox.other2tess.other2tess import other2tess
from Toolbox.tess2other.tess2other import tess2other
from Toolbox.link_processing import link_processing


class MyUIAPI(QMainWindow):
    def __init__(self, parent = None):
        super(MyUIAPI, self).__init__(parent)
        self.ui = MyUI()
        self.ui.setupUi(self)
        self.createConnect()
        
        # 功能组状态
        self.state_grout_input = True
        self.state_grout_output = True
        self.state_grout_traj = True
        self.state_grout_link = True

        # 用于保存车辆轨迹
        # 是否保存为json
        sys.modules["__main__"].__dict__["state_exportJson"] = self.ui.checkbox_traj_exportJson
        # 是否上传至kafka
        sys.modules["__main__"].__dict__["state_exportKafka"] = self.ui.checkbox_traj_exportKafka
        # 保存为json的位置
        sys.modules["__main__"].__dict__["location_exportJson"] = os.path.dirname(os.path.abspath(__file__)) + "\\..\\WorkSpace\\Data"
        # 上传至kafka的位置
        sys.modules["__main__"].__dict__["location_exportKafka"] = {
            "IP": self.ui.text_traj_kafkaIP,
            "port": self.ui.text_traj_kafkaPort,
            "topic": self.ui.text_traj_kafkaTopic,
        }
        # 投影中心经纬度
        sys.modules["__main__"].__dict__["lon_and_lat"] = {
            "lon": self.ui.text_output_centerLon,
            "lat": self.ui.text_output_centerLat
        }
        # 提示窗函数
        sys.modules["__main__"].__dict__["function_showInfoBox"] = self.showInfoBox

        # # 有些分组默认不显示
        # self.group_input()
        # self.group_output()
        # self.group_traj()
        # self.group_link()


    # 关联起按键和函数
    def createConnect(self):
        # 〇、锦上添花
        self.ui.btn_input_title_view.clicked.connect(self.group_input)
        self.ui.btn_output_title_view.clicked.connect(self.group_output)
        self.ui.btn_traj_title_view.clicked.connect(self.group_traj)
        self.ui.btn_link_title_view.clicked.connect(self.group_link)

        # 一、导入
        self.ui.btn_input_excel.clicked.connect(self.Excel2Tess)
        self.ui.btn_input_opendrive.clicked.connect(self.Opendrive2Tess)
        self.ui.btn_input_shape.clicked.connect(self.Shape2Tess)
        self.ui.btn_input_osm.clicked.connect(self.Osm2Tess)

        # 二、导出
        self.ui.btn_output_opendrive.clicked.connect(self.Tess2Opendrive)
        self.ui.btn_output_shape.clicked.connect(self.Tess2Shape)
        self.ui.btn_output_geojson.clicked.connect(self.Tess2Geojson)
        self.ui.btn_output_unity.clicked.connect(self.Tess2Unity)
        self.ui.btn_output_json.clicked.connect(self.Tess2Json)

        # 三、轨迹
        self.ui.btn_traj_viewTrajPath.clicked.connect(self.viewTrajPath)
        self.ui.btn_traj_changeTrajPath.clicked.connect(self.changeTrajPath)

        # 四、路段
        self.ui.btn_link_create.clicked.connect(self.createLink)
        self.ui.btn_link_split.clicked.connect(self.splitLink)
        self.ui.btn_link_join.clicked.connect(self.joinLink)
        self.ui.btn_link_simplify.clicked.connect(self.simplifyTessngFile)

    ###########################################################################

    # 选择打开文件路径
    def openFile(self, formats, suffixs):
        # 指定文件后缀
        xodrSuffix = ";;".join([f"{formats[i]} Files (*.{suffixs[i]})" for i in range(len(formats))])
        # 默认读取位置
        dbDir = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "WorkSpace", "Data")
        # 弹出文件选择框
        file_path, filtr = QFileDialog.getOpenFileName(None, "打开文件", dbDir, xodrSuffix)
        
        return file_path

    # 选择打开文件夹路径
    def openFolder(self, ):
        # 默认读取位置
        dbDir = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "WorkSpace", "Data")
        # 弹出文件选择框
        file_path = QFileDialog.getExistingDirectory(None, "打开文件夹", dbDir)
        
        return file_path

    #选择保存文件路径
    def saveFile(self, format_, suffix):
        # 指定文件后缀
        xodrSuffix = f"{format_} Files (*.{suffix})"
        # 默认保存位置
        dbDir = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "WorkSpace", "Data")
        # 弹出文件选择框
        file_path, filtr = QFileDialog.getSaveFileName(None, "保存文件", dbDir, xodrSuffix)
        
        return file_path

    # 信息窗显示信息
    def showInfo(self, info):
        self.ui.txt_message.clear()
        self.ui.txt_message.setText(str(info))

    # 弹出警告或提示提示框
    def showInfoBox(self, content, mode="info"):
        msg_box = QMessageBox()
        if mode == "warning":
            msg_box.setWindowTitle("警告")
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setWindowTitle("提示")
            msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(content)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    # 获取投影中心经纬度
    def getCentralCoordinate(self, ):
        lon_str = self.ui.text_output_centerLon.text()
        lat_str = self.ui.text_output_centerLat.text()
        
        if not lon_str or not lat_str:
            self.showInfoBox("请输入投影中心经度和纬度！")
            return None, None
        
        try:
            lon_float = float(lon_str)
            lat_float = float(lat_str)
        except:
            self.showInfoBox("请输入数字！")
            return None, None
        
        if not (-180<lon_float<180) or not (-90<lat_float<90):
            self.showInfoBox("请输入合理经纬度！")
            return None, None
        
        return lon_float, lat_float

    # 获取投影中心经纬度（osm）
    def getCentralCoordinate_osm(self, ):
        lon_str = self.ui.text_input_osm_lon.text()
        lat_str = self.ui.text_input_osm_lat.text()

        if not lon_str or not lat_str:
            self.showInfoBox("请输入中心位置经度和纬度！")
            return None, None

        try:
            lon_float = float(lon_str)
            lat_float = float(lat_str)
        except:
            self.showInfoBox("请输入数字！")
            return None, None

        if not (-180 < lon_float < 180) or not (-90 < lat_float < 90):
            self.showInfoBox("请输入合理经纬度！")
            return None, None

        return lon_float, lat_float

    # 是否使用投影的弹窗
    def showConfirmDialog(self, messages):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Choice")
        msg_box.setText(messages["content"])

        # 设置按钮
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        # 设置默认选项
        msg_box.setDefaultButton(QMessageBox.Cancel)
        # 修改按钮上的文本
        msg_box.button(QMessageBox.Yes).setText(messages["yes"])
        msg_box.button(QMessageBox.No).setText(messages["no"])
        msg_box.button(QMessageBox.Cancel).setText("取消")
        # 获取选择结果
        result = msg_box.exec_()

        return result


    ######################################################################
    # 一、导入外部数据源创建路网

    # (1)导入excel
    def Excel2Tess(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.正在仿真中无法导入
        if iface.simuInterface().isRunning():
            self.showInfoBox("请先停止仿真！", "warning")
            return

        # 2.选择输入路径
        file_path = self.openFile(["Excel", "CSV"], ["xlsx", "csv"])
        if not file_path:
            return

        # 3.执行转换
        parms = {
            "file_path": file_path,
        }
        try:
            error_message = other2tess(netiface, parms, "excel")
            self.showInfo(error_message)
            self.showInfoBox("Importing Excel is successful !")
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.showInfo(error_message)
            print(error_message)
            self.showInfoBox("Importing Excel is failed !", "warning")

    # (2)导入opendrive
    def Opendrive2Tess(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.正在仿真中无法导入
        if iface.simuInterface().isRunning():
            self.showInfoBox("请先停止仿真！", "warning")
            return

        # 2.选择车道类型
        lane_types = []
        for choiceLaneType in self.ui.checkbox_intput_opendrive_laneTypes:
            if choiceLaneType.isChecked():
                lane_types.append(choiceLaneType.text())
        if not lane_types:
            self.showInfoBox("请至少选择一种车道类型！", "warning")
            return 
        
        # 3.选择分段长度
        step_length = float(self.ui.combo_input_opendrive_step.currentText().split(" ")[0])
        
        # 4.选择输入路径
        file_path = self.openFile(["OpenDrive"], ["xodr"])
        if not file_path:
            return
        
        # 5.执行转换
        parms = {
            "file_path": file_path,
            "step_length": step_length,
            "lane_types": lane_types
            }
        try:
            error_message = other2tess(netiface, parms, "opendrive")
            self.showInfo(error_message)
            self.showInfoBox("Importing OpenDrive is successful !")
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.showInfo(error_message)
            print(error_message)
            self.showInfoBox("Importing OpenDrive is failed !", "warning")

    # (3)导入shape
    def Shape2Tess(self,):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.正在仿真中无法导入
        if iface.simuInterface().isRunning():
            self.showInfoBox("请先停止仿真！", "warning")
            return

        # 2.坐标相关
        confirm = self.showConfirmDialog({"content": "请选择读取的坐标的类型！", "yes": "经纬度坐标", "no": "平面坐标"})
        if confirm == QMessageBox.Yes:
            is_use_lon_and_lat = True
        elif confirm == QMessageBox.No:
            is_use_lon_and_lat = False
        else:
            return

        # 3.获取车道和车道连接文件名
        laneFileName = self.ui.text_intput_shape_lane.text()
        laneConnectorFileName = self.ui.text_intput_shape_laneConnector.text()
        if not laneFileName:
            self.showInfoBox("请输入车道文件名！", "warning")
            return

        # 4.选择导入中心线还是边界线
        if self.ui.radio_intput_shape_importMode_1.isChecked():
            is_use_center_line = True
        elif self.ui.radio_intput_shape_importMode_2.isChecked():
            is_use_center_line = False
        else:
            return
        
        # 5.选择输入路径
        folder_path = self.openFolder()
        if not folder_path:
            return
        
        # 6.执行转换
        parms = {
            "folder_path": folder_path,
            "is_use_lon_and_lat": is_use_lon_and_lat,
            "is_use_center_line": is_use_center_line,
            "laneFileName": laneFileName,
            "laneConnectorFileName": laneConnectorFileName
            }
        try:
            error_message = other2tess(netiface, parms, "shape")
            self.showInfo(error_message)
            self.showInfoBox("Importing Shapefile is successful !")
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.showInfo(error_message)
            print(error_message)
            self.showInfoBox("Importing Shapefile is failed !", "warning")
    
    # (4)导入osm
    def Osm2Tess(self,):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.正在仿真中无法导入
        if iface.simuInterface().isRunning():
            self.showInfoBox("请先停止仿真！", "warning")
            return
        
        # 2.获取中心位置经纬度
        lon_0, lat_0 = self.getCentralCoordinate_osm()
        if not lon_0 or not lat_0:
            return

        # 3.获取范围大小
        distance = float(self.ui.combo_input_osm_length.currentText().split(" ")[0])

        # 4.执行转换
        parms = {
            "lon_0": lon_0,
            "lat_0": lat_0,
            "distance": distance
            }
        try:
            error_message = other2tess(netiface, parms, "osm")
            self.showInfo(error_message)
            self.showInfoBox("Importing OpenStreetMap is successful !")
        except Exception as e:
            error_message = str(traceback.format_exc())
            self.showInfo(error_message)
            print(error_message)
            self.showInfoBox("Importing OpenStreetMap is failed !", "warning")


    ######################################################################
    # 二、导出路网为特定格式

    # (1)导出为opendrive
    def Tess2Opendrive(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.检查路网上是否有路段
        if netiface.linkCount() == 0:
            self.showInfoBox("当前路网没有路段 !", "warning")
            return

        # 2.投影相关
        confirm = self.showConfirmDialog({"content": "请选择是否将投影中心的经纬度写入header！", "yes":"是", "no":"否"})
        if confirm == QMessageBox.Yes:
            # 获取投影中心经纬度
            lon_0, lat_0 = self.getCentralCoordinate()
            if not lon_0 or not lat_0:
                return
        elif confirm == QMessageBox.No:
            lon_0, lat_0 = None, None
        else:
            return

        # 3.选择输出路径
        file_path = self.saveFile("OpenDrive", "xodr")
        if not file_path:
            return
        
        # 4.执行转换
        parms = {
            "file_path": file_path,
            "lon_0": lon_0,
            "lat_0": lat_0
            }
        tess2other(netiface, parms, "opendrive")
        
        # 5.显示成功信息
        self.showInfoBox("Exporting OpenDrive is successful !")

    # (2)导出为shape
    def Tess2Shape(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.检查路网上是否有路段
        if netiface.linkCount() == 0:
            self.showInfoBox("当前路网没有路段 !", "warning")
            return

        # 2.投影相关
        confirm = self.showConfirmDialog({"content": "请选择写入的坐标的类型！", "yes":"经纬度坐标", "no":"平面坐标"})
        if confirm == QMessageBox.Yes:
            # 获取投影中心经纬度
            lon_0, lat_0 = self.getCentralCoordinate()
            if not lon_0 or not lat_0:
                return
        elif confirm == QMessageBox.No:
            lon_0, lat_0 = None, None
        else:
            return
        
        # 3.选择输出路径
        file_path = self.saveFile("Shapefile", "shp")
        if not file_path:
            return
        
        # 4.执行转换
        parms = {
            "file_path": file_path,
            "lon_0": lon_0,
            "lat_0": lat_0
            }
        tess2other(netiface, parms, "shape")
        
        # 5.显示成功信息
        self.showInfoBox("Exporting Shape is successful !")

    # (3)导出为geojson
    def Tess2Geojson(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.检查路网上是否有路段
        if netiface.linkCount() == 0:
            self.showInfoBox("当前路网没有路段 !", "warning")
            return

        # 2.投影相关
        confirm = self.showConfirmDialog({"content": "请选择写入的坐标的类型！", "yes":"经纬度坐标", "no":"平面坐标"})
        if confirm == QMessageBox.Yes:
            # 获取投影中心经纬度
            lon_0, lat_0 = self.getCentralCoordinate()
            if not lon_0 or not lat_0:
                return
        elif confirm == QMessageBox.No:
            lon_0, lat_0 = None, None
        else:
            return

        # 3.选择输出路径
        file_path = self.saveFile("GeoJson", "geojson")
        if not file_path:
            return
        
        # 4.执行转换
        parms = {
            "file_path": file_path,
            "lon_0": lon_0,
            "lat_0": lat_0
            }
        tess2other(netiface, parms, "geojson")
        
        # 5.显示成功信息
        self.showInfoBox("Exporting GeoJson is successful !")

    # (4)导出为unity
    def Tess2Unity(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.检查路网上是否有路段
        if netiface.linkCount() == 0:
            self.showInfoBox("当前路网没有路段 !", "warning")
            return
        
        # 2.选择输出路径
        file_path = self.saveFile("Json", "json")
        if not file_path:
            return
        
        # 3.执行转换
        parms = {
            "file_path": file_path
            }
        tess2other(netiface, parms, "unity")
        
        # 4.显示成功信息
        self.showInfoBox("Exporting Unity is successful !")

    # (5)导出为json(标准格式)
    def Tess2Json(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.检查路网上是否有路段
        if netiface.linkCount() == 0:
            self.showInfoBox("当前路网没有路段 !", "warning")
            return

        # 2.投影相关
        confirm = self.showConfirmDialog({"content": "请选择是否写入经纬度坐标！", "yes":"是", "no":"否"})
        if confirm == QMessageBox.Yes:
            # 获取投影中心经纬度
            lon_0, lat_0 = self.getCentralCoordinate()
            if not lon_0 or not lat_0:
                return
        elif confirm == QMessageBox.No:
            lon_0, lat_0 = None, None
        else:
            return
        
        # 3.选择输出路径
        file_path = self.saveFile("Json", "json")
        if not file_path:
            return
        
        # 4.执行转换
        parms = {
            "file_path": file_path,
            "lon_0": lon_0,
            "lat_0": lat_0
            }
        tess2other(netiface, parms, "json")
        
        # 5.显示成功信息
        self.showInfoBox("Exporting Json is successful !")

    ###########################################################################
    # 三、轨迹输出

    # (1)查看轨迹文件保存地址
    def viewTrajPath(self, ):
        traj_path = sys.modules["__main__"].__dict__["location_exportJson"]
        self.showInfoBox(f"当前设定保存位置为：{os.path.normpath(traj_path)}")

    # (2)更改轨迹文件保存地址
    def changeTrajPath(self, ):
        folder_path = self.openFolder()
        if not folder_path:
            return
        sys.modules["__main__"].__dict__["location_exportJson"] = folder_path


    ###########################################################################
    # 四、路段处理

    # (1)创建路段
    def createLink(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.获取输入框信息
        input_info = self.ui.text_link_create.text()

        # 2.执行创建
        state, message = link_processing.createLink(netiface, input_info)

        # 3.显示信息
        if state:
            self.showInfoBox("创建结束！")
        else:
            self.showInfoBox(message, "warning")

    # (2)打断路段
    def splitLink(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # 1.获取输入框信息
        input_info = self.ui.text_link_split.text()

        # 2.执行打断
        state, message = link_processing.splitLink(netiface, input_info)

        # 3.显示信息
        if state:
            self.showInfo(message)
            self.showInfoBox("打断结束！")
        else:
            self.showInfoBox(message, "warning")

    # (3)连接路段
    def joinLink(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.执行连接
        state, message = link_processing.joinLink(netiface)

        # 2.显示信息
        if state:
            self.showInfo(message)
            self.showInfoBox("路段连接结束！")
        else:
            self.showInfoBox(message, "warning")

    # (4)简化路网
    def simplifyTessngFile(self, ):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.执行简化
        state, message = link_processing.simplifyTessngFile(netiface)

        # 2.显示信息
        if state:
            self.showInfo(message)
            self.showInfoBox("已经在同一目录下生成简化版路网，且当前已经打开！")
        else:
            self.showInfoBox(message, "warning")


    ###########################################################################
    # 其他

    # 【导入分组】的收起或展开
    def group_input(self, ):
        if self.state_grout_input:
            self.state_grout_input = False
            self.ui.btn_input_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '展开◀', None))
            for unit in self.ui.group_input:
                unit.setVisible(False)
        else:
            self.state_grout_input = True
            self.ui.btn_input_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
            for unit in self.ui.group_input:
                unit.setVisible(True)

    # 【导出分组】的收起或展开
    def group_output(self, ):
        if self.state_grout_output:
            self.state_grout_output = False
            self.ui.btn_output_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '展开◀', None))
            for unit in self.ui.group_output:
                unit.setVisible(False)
        else:
            self.state_grout_output = True
            self.ui.btn_output_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
            for unit in self.ui.group_output:
                unit.setVisible(True)

    # 【轨迹分组】的收起或展开
    def group_traj(self, ):
        if self.state_grout_traj:
            self.state_grout_traj = False
            self.ui.btn_traj_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '展开◀', None))
            for unit in self.ui.group_traj:
                unit.setVisible(False)
        else:
            self.state_grout_traj = True
            self.ui.btn_traj_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
            for unit in self.ui.group_traj:
                unit.setVisible(True)

    # 【路段分组】的收起或展开
    def group_link(self, ):
        if self.state_grout_link:
            self.state_grout_link = False
            self.ui.btn_link_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '展开◀', None))
            for unit in self.ui.group_link:
                unit.setVisible(False)
        else:
            self.state_grout_link = True
            self.ui.btn_link_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
            for unit in self.ui.group_link:
                unit.setVisible(True)
