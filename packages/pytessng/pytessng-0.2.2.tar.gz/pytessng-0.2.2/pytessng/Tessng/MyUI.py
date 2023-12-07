from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


# 标题字体
font_title = QFont()
font_title.setFamily("微软雅黑")
font_title.setPointSize(15)
# 内容字体
font_content = QFont()
font_content.setFamily("SimSun")
font_content.setPointSize(12)

class MyUI(object):
    def setupUi(self, MyUIAPI_Class):
        if not MyUIAPI_Class.objectName():
            MyUIAPI_Class.setObjectName(u"MyUIAPI_Class")
        # MyUIAPI_Class.resize(100, 200)
        
        #######################################################################
        
        # 【主窗口】的【界面】
        self.centralWidget = QWidget(MyUIAPI_Class)
        self.centralWidget.setObjectName(u"centralWidget")
        # self.centralWidget.setFixedWidth(420)
        MyUIAPI_Class.setCentralWidget(self.centralWidget)

        # 【主窗口】的【布局管理器】
        self.verticalLayout_center = QVBoxLayout(self.centralWidget)
        self.verticalLayout_center.setSpacing(12)
        self.verticalLayout_center.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_center.setObjectName(u"verticalLayout_center")
        self.verticalLayout_center.setAlignment(Qt.AlignTop)

        #######################################################################

        # 1.【导入外部数据源的功能分组】的【界面】
        self.groupBox_input = QGroupBox(self.centralWidget)
        self.groupBox_input.setObjectName(u"groupBox_input")
        self.verticalLayout_center.addWidget(self.groupBox_input)
        # self.groupBox_input.setFixedWidth(400)

        # 1.【导入外部数据源的功能分组】的【布局管理器】
        self.verticalLayout_input = QVBoxLayout(self.groupBox_input)
        self.verticalLayout_input.setSpacing(11)
        self.verticalLayout_input.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_input.setObjectName(u"verticalLayout_input")

        # 1.【导入外部数据源的功能分组】的【标题】
        self.horizontalLayout_input_title = QHBoxLayout()
        # 文本框
        self.label_input_title = QLabel("一、导入外部数据源创建路网")
        self.label_input_title.setFont(font_title)
        self.label_input_title.setStyleSheet("color: red")
        self.horizontalLayout_input_title.addWidget(self.label_input_title)
        # 按钮
        self.btn_input_title_view = QPushButton()
        self.btn_input_title_view.setObjectName(u"btn_intput_title_view")
        self.btn_input_title_view.setFixedWidth(90)
        self.horizontalLayout_input_title.addWidget(self.btn_input_title_view)
        # 加入垂直布局
        self.verticalLayout_input.addLayout(self.horizontalLayout_input_title)

        # 1.1.【导入excel】的按键
        self.btn_input_excel = QPushButton(self.centralWidget)
        self.btn_input_excel.setObjectName(u"btn_input_excel")
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.btn_input_excel)

        # 创建一条横线
        self.horizontalLine_intput_1 = QFrame()
        self.horizontalLine_intput_1.setFrameShape(QFrame.HLine)  # 设置为横向线条
        self.horizontalLine_intput_1.setFrameShadow(QFrame.Sunken)  # 设置线条样式
        self.horizontalLine_intput_1.setStyleSheet(
            "QFrame { "
            "   background-color: dodgerblue; "  # 设置颜色为红色
            "   border: 2px dashed white; "  # 设置粗细和虚线样式
            "}"
        )
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.horizontalLine_intput_1)

        # 1.2.【导入OpenDrive】的【分段下拉框】
        self.horizontalLayout_input_opendrive_1 = QHBoxLayout()
        # 文本框
        self.label_input_opendrive_step = QLabel("路段最小分段长度：")
        self.horizontalLayout_input_opendrive_1.addWidget(self.label_input_opendrive_step)
        # 下拉单选框
        self.combo_input_opendrive_step = QComboBox()
        self.combo_input_opendrive_step.addItems(("1 m", "0.5 m", "5 m", "10 m", "20 m"))
        self.horizontalLayout_input_opendrive_1.addWidget(self.combo_input_opendrive_step)
        # 加入垂直布局
        # self.horizontalLayout_input_opendrive_1.addStretch()
        self.verticalLayout_input.addLayout(self.horizontalLayout_input_opendrive_1)
        
        # 1.2.【导入OpenDrive】的【车道复选框】
        self.horizontalLayout_input_opendrive_2 = QHBoxLayout()
        # 多选框
        self.checkbox_intput_opendrive_laneType_1 = QCheckBox('机动车道')
        self.checkbox_intput_opendrive_laneType_2 = QCheckBox('非机动车道')
        self.checkbox_intput_opendrive_laneType_3 = QCheckBox('人行道')
        self.checkbox_intput_opendrive_laneType_4 = QCheckBox('应急车道')
        self.checkbox_intput_opendrive_laneTypes = [
            self.checkbox_intput_opendrive_laneType_1,
            self.checkbox_intput_opendrive_laneType_2,
            self.checkbox_intput_opendrive_laneType_3,
            self.checkbox_intput_opendrive_laneType_4
        ]
        for checkbox in self.checkbox_intput_opendrive_laneTypes:
            checkbox.setCheckState(Qt.Checked)
            self.horizontalLayout_input_opendrive_2.addWidget(checkbox)
        # 加入垂直布局
        self.horizontalLayout_input_opendrive_2.addStretch()
        self.verticalLayout_input.addLayout(self.horizontalLayout_input_opendrive_2)
        
        # 1.2.【导入OpenDrive】的【按键】
        self.btn_input_opendrive = QPushButton(self.centralWidget)
        self.btn_input_opendrive.setObjectName(u"btn_input_opendrive")
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.btn_input_opendrive)

        # 创建一条横线
        self.horizontalLine_intput_2 = QFrame()
        self.horizontalLine_intput_2.setFrameShape(QFrame.HLine)  # 设置为横向线条
        self.horizontalLine_intput_2.setFrameShadow(QFrame.Sunken)  # 设置线条样式
        self.horizontalLine_intput_2.setStyleSheet(
            "QFrame { "
            "   background-color: dodgerblue; "  # 设置颜色为红色
            "   border: 2px dashed white; "  # 设置粗细和虚线样式
            "}"
        )
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.horizontalLine_intput_2)

        # 1.3.【文件名】的【输入框】
        self.horizontalLayout_intput_shape_1 = QHBoxLayout()
        # 文本框
        self.label_intput_shape_fileName = QLabel("文件名：")
        self.label_intput_shape_fileName.setMaximumWidth(80)
        self.horizontalLayout_intput_shape_1.addWidget(self.label_intput_shape_fileName)
        # 输入框
        self.text_intput_shape_lane = QLineEdit(self.centralWidget)
        self.text_intput_shape_lane.setPlaceholderText("车道文件名")
        self.text_intput_shape_lane.setText("lane")
        self.horizontalLayout_intput_shape_1.addWidget(self.text_intput_shape_lane)
        # 输入框
        self.text_intput_shape_laneConnector = QLineEdit(self.centralWidget)
        self.text_intput_shape_laneConnector.setPlaceholderText("车辆连接文件名")
        self.text_intput_shape_laneConnector.setText("laneConnector")
        self.horizontalLayout_intput_shape_1.addWidget(self.text_intput_shape_laneConnector)
        # 加入垂直布局
        # self.horizontalLayout_intput_shape_1.addStretch()
        self.verticalLayout_input.addLayout(self.horizontalLayout_intput_shape_1)

        # 1.3.【导入shape】的【单选框】
        self.horizontalLayout_intput_shape_2 = QHBoxLayout()
        # 单选框
        self.radio_intput_shape_importMode_1 = QRadioButton("导入车道中心线")
        self.horizontalLayout_intput_shape_2.addWidget(self.radio_intput_shape_importMode_1)
        self.radio_intput_shape_importMode_1.setChecked(True)
        # 单选框
        self.radio_intput_shape_importMode_2 = QRadioButton("导入车道边界线")
        self.horizontalLayout_intput_shape_2.addWidget(self.radio_intput_shape_importMode_2)
        # 加入垂直布局
        self.verticalLayout_input.addLayout(self.horizontalLayout_intput_shape_2)
        
        # 1.3.【导入shape】的按键
        self.btn_input_shape = QPushButton(self.centralWidget)
        self.btn_input_shape.setObjectName(u"btn_input_shape")
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.btn_input_shape)
        
        # 创建一条横线
        self.horizontalLine_intput_3 = QFrame()
        self.horizontalLine_intput_3.setFrameShape(QFrame.HLine)  # 设置为横向线条
        self.horizontalLine_intput_3.setFrameShadow(QFrame.Sunken)  # 设置线条样式
        self.horizontalLine_intput_3.setStyleSheet(
            "QFrame { "
            "   background-color: dodgerblue; "  # 设置颜色为红色
            "   border: 2px dashed white; "  # 设置粗细和虚线样式
            "}"
        )
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.horizontalLine_intput_3)

        # 1.4.【中心经纬度】的【输入框】
        self.horizontalLayout_intput_osm_1 = QHBoxLayout()
        # 文本框
        self.label_input_osm_center = QLabel("中心位置经纬度：")
        # self.label_input_osm_center.setMaximumWidth(130)
        self.horizontalLayout_intput_osm_1.addWidget(self.label_input_osm_center)
        # 输入框
        self.text_input_osm_lon = QLineEdit(self.centralWidget)
        self.text_input_osm_lon.setPlaceholderText("经度")
        self.horizontalLayout_intput_osm_1.addWidget(self.text_input_osm_lon)
        # 输入框
        self.text_input_osm_lat = QLineEdit(self.centralWidget)
        self.text_input_osm_lat.setPlaceholderText("纬度")
        self.horizontalLayout_intput_osm_1.addWidget(self.text_input_osm_lat)
        # 加入垂直布局
        self.verticalLayout_input.addLayout(self.horizontalLayout_intput_osm_1)

        # 1.4.【范围大小】的【输入框】
        self.horizontalLayout_intput_osm_2 = QHBoxLayout()
        # 文本框
        self.label_input_osm_length = QLabel("导入范围半径：")
        # self.label_input_osm_length.setMaximumWidth(130)
        self.horizontalLayout_intput_osm_2.addWidget(self.label_input_osm_length)
        # 下拉框
        self.combo_input_osm_length = QComboBox()
        self.combo_input_osm_length.addItems(("0.5 km", "1 km", "2 km", "3 km", "4 km", "5 km", "6 km", "7 km", "8 km", "9 km", "10 km"))
        self.horizontalLayout_intput_osm_2.addWidget(self.combo_input_osm_length)
        # 加入垂直布局
        # self.horizontalLayout_intput_osm_2.addStretch()
        self.verticalLayout_input.addLayout(self.horizontalLayout_intput_osm_2)

        # 1.4.【导入osm】的按键
        self.btn_input_osm = QPushButton(self.centralWidget)
        self.btn_input_osm.setObjectName(u"btn_input_osm")
        # 加入垂直布局
        self.verticalLayout_input.addWidget(self.btn_input_osm)

        # 除了标题之外的组件
        self.group_input = [
            self.btn_input_excel,
            self.horizontalLine_intput_1,
            self.label_input_opendrive_step,
            self.combo_input_opendrive_step,
            self.checkbox_intput_opendrive_laneType_1,
            self.checkbox_intput_opendrive_laneType_2,
            self.checkbox_intput_opendrive_laneType_3,
            self.checkbox_intput_opendrive_laneType_4,
            self.btn_input_opendrive,
            self.horizontalLine_intput_2,
            self.label_intput_shape_fileName,
            self.text_intput_shape_lane,
            self.text_intput_shape_laneConnector,
            self.radio_intput_shape_importMode_1,
            self.radio_intput_shape_importMode_2,
            self.btn_input_shape,
            self.horizontalLine_intput_3,
            self.label_input_osm_center,
            self.text_input_osm_lon,
            self.text_input_osm_lat,
            self.label_input_osm_length,
            self.combo_input_osm_length,
            self.btn_input_osm,
        ]

        #######################################################################

        # 2.【导出为特定格式的功能分组】的界面
        self.groupBox_output = QGroupBox(self.centralWidget)
        self.groupBox_output.setObjectName(u"groupBox_output")
        self.verticalLayout_center.addWidget(self.groupBox_output)
        # self.groupBox_output.setFixedWidth(400)

        # 2.【导出为特定格式的功能分组】的布局管理器
        self.verticalLayout_output = QVBoxLayout(self.groupBox_output)
        self.verticalLayout_output.setSpacing(11)
        self.verticalLayout_output.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_output.setObjectName(u"verticalLayout_output")

        # 2.【导出为特定格式的功能分组】的标题
        self.horizontalLayout_output_title = QHBoxLayout()
        # 文本框
        self.label_output_title = QLabel("二、导出当前路网为特定格式")
        self.label_output_title.setFont(font_title)
        self.label_output_title.setStyleSheet("color: red;")
        self.horizontalLayout_output_title.addWidget(self.label_output_title)
        # 按钮
        self.btn_output_title_view = QPushButton()
        self.btn_output_title_view.setObjectName(u"btnInputTitle")
        self.btn_output_title_view.setFixedWidth(90)
        self.horizontalLayout_output_title.addWidget(self.btn_output_title_view)
        # 加入垂直布局
        self.verticalLayout_output.addLayout(self.horizontalLayout_output_title)

        # 2.0.【投影中心经纬度】的【输入框】
        self.horizontalLayout_output_center = QHBoxLayout()
        # 文本框
        self.label_output_center = QLabel("墨卡托投影：")
        self.label_output_center.setMaximumWidth(130)
        self.horizontalLayout_output_center.addWidget(self.label_output_center)
        # 输入框
        self.text_output_centerLon = QLineEdit(self.centralWidget)
        self.text_output_centerLon.setPlaceholderText("投影中心经度")
        # self.text_output_centerLon.setMaximumWidth(185)
        self.horizontalLayout_output_center.addWidget(self.text_output_centerLon)
        # 输入框
        self.text_output_centerLat = QLineEdit(self.centralWidget)
        self.text_output_centerLat.setPlaceholderText("投影中心纬度")
        # self.text_output_centerLat.setMaximumWidth(185)
        self.horizontalLayout_output_center.addWidget(self.text_output_centerLat)
        # 加入垂直布局
        self.verticalLayout_output.addLayout(self.horizontalLayout_output_center)

        # 2.1.【导出OpenDrive】的按键
        self.btn_output_opendrive = QPushButton(self.centralWidget)
        self.btn_output_opendrive.setObjectName(u"btn_output_opendrive")
        # 加入垂直布局
        self.verticalLayout_output.addWidget(self.btn_output_opendrive)

        # 2.2.【导出Shape】的按键
        self.btn_output_shape = QPushButton(self.centralWidget)
        self.btn_output_shape.setObjectName(u"btn_output_shape")
        # 加入垂直布局
        self.verticalLayout_output.addWidget(self.btn_output_shape)

        # 2.3.【导出GeoJson】的按键
        self.btn_output_geojson = QPushButton(self.centralWidget)
        self.btn_output_geojson.setObjectName(u"btn_output_geojson")
        # 加入垂直布局
        self.verticalLayout_output.addWidget(self.btn_output_geojson)

        # 2.4.【导出Unity】的按键
        self.btn_output_unity = QPushButton(self.centralWidget)
        self.btn_output_unity.setObjectName(u"btn_output_unity")
        # 加入垂直布局
        self.verticalLayout_output.addWidget(self.btn_output_unity)

        # 2.5.【导出Json】的按键
        self.btn_output_json = QPushButton(self.centralWidget)
        self.btn_output_json.setObjectName(u"btn_output_json")
        # 加入垂直布局
        self.verticalLayout_output.addWidget(self.btn_output_json)

        # 除了标题之外的组件
        self.group_output = [
            self.label_output_center,
            self.text_output_centerLon,
            self.text_output_centerLat,
            self.btn_output_opendrive,
            self.btn_output_shape,
            self.btn_output_geojson,
            self.btn_output_unity,
            self.btn_output_json,
            ]

        #######################################################################

        # 3.【导出车辆轨迹】的界面
        self.groupBox_traj = QGroupBox(self.centralWidget)
        self.groupBox_traj.setObjectName(u"groupBox_traj")
        self.verticalLayout_center.addWidget(self.groupBox_traj)
        # self.groupBox_traj.setFixedWidth(400)

        # 3.【导出车辆轨迹】的布局管理器
        self.verticalLayout_traj = QVBoxLayout(self.groupBox_traj)
        self.verticalLayout_traj.setSpacing(11)
        self.verticalLayout_traj.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_traj.setObjectName(u"verticalLayout_traj")

        # 3.【导出车辆轨迹】的标题
        self.horizontalLayout_traj_title = QHBoxLayout()
        # 文本框
        self.label_traj_title = QLabel("三、输出标准车辆轨迹")
        self.label_traj_title.setFont(font_title)
        self.label_traj_title.setStyleSheet("color: red;")
        self.horizontalLayout_traj_title.addWidget(self.label_traj_title)
        # 按钮
        self.btn_traj_title_view = QPushButton()
        self.btn_traj_title_view.setObjectName(u"btn_traj_title_view")
        self.btn_traj_title_view.setFixedWidth(90)
        self.horizontalLayout_traj_title.addWidget(self.btn_traj_title_view)
        # 加入垂直布局
        self.verticalLayout_traj.addLayout(self.horizontalLayout_traj_title)

        # 3.1.【车辆轨迹保存为json】
        self.horizontalLayout_traj_json = QHBoxLayout()
        # 【输出标准轨迹】的【单选框】
        self.checkbox_traj_exportJson = QCheckBox("保存为json")
        # self.checkbox_traj_exportJson.setCheckState(Qt.Checked)
        self.horizontalLayout_traj_json.addWidget(self.checkbox_traj_exportJson)
        # 【查看保存路径】的【按钮】
        self.btn_traj_viewTrajPath = QPushButton(self.centralWidget)
        self.btn_traj_viewTrajPath.setObjectName(u"btn_traj_viewTrajPath")
        self.horizontalLayout_traj_json.addWidget(self.btn_traj_viewTrajPath)
        # 【更改保存路径】的【按钮】
        self.btn_traj_changeTrajPath = QPushButton(self.centralWidget)
        self.btn_traj_changeTrajPath.setObjectName(u"btn_traj_changeTrajPath")
        self.horizontalLayout_traj_json.addWidget(self.btn_traj_changeTrajPath)
        # 加入垂直布局
        self.verticalLayout_traj.addLayout(self.horizontalLayout_traj_json)

        # 3.2.【车辆轨迹上传至kafka】
        self.horizontalLayout_traj_kafka = QHBoxLayout()
        # 【输出标准轨迹】的【单选框】
        self.checkbox_traj_exportKafka = QCheckBox("上传至kafka")
        # self.checkbox_traj_exportKafka.setCheckState(Qt.Checked)
        self.horizontalLayout_traj_kafka.addWidget(self.checkbox_traj_exportKafka)
        # 【IP】的【输入框】
        self.text_traj_kafkaIP = QLineEdit(self.centralWidget)
        self.text_traj_kafkaIP.setPlaceholderText("IP")
        self.horizontalLayout_traj_kafka.addWidget(self.text_traj_kafkaIP)
        # 【端口】的【输入框】
        self.text_traj_kafkaPort = QLineEdit(self.centralWidget)
        self.text_traj_kafkaPort.setPlaceholderText("端口")
        self.text_traj_kafkaPort.setFixedWidth(70)
        self.horizontalLayout_traj_kafka.addWidget(self.text_traj_kafkaPort)
        # 加入垂直布局
        self.verticalLayout_traj.addLayout(self.horizontalLayout_traj_kafka)
        # 【topic】的【输入框】
        self.text_traj_kafkaTopic = QLineEdit(self.centralWidget)
        self.text_traj_kafkaTopic.setPlaceholderText("topic")
        self.verticalLayout_traj.addWidget(self.text_traj_kafkaTopic)

        # 除了标题之外的组件
        self.group_traj = [
            self.checkbox_traj_exportJson,
            self.btn_traj_viewTrajPath,
            self.btn_traj_changeTrajPath,
            self.checkbox_traj_exportKafka,
            self.text_traj_kafkaIP,
            self.text_traj_kafkaPort,
            self.text_traj_kafkaTopic
        ]

        #######################################################################

        # 4.【路段处理的功能分组】的界面
        self.groupBox_link = QGroupBox(self.centralWidget)
        self.groupBox_link.setObjectName(u"groupBox_link")
        self.verticalLayout_center.addWidget(self.groupBox_link)
        # self.groupBox_link.setFixedWidth(400)

        # 4.【路段处理的功能分组】的布局管理器
        self.verticalLayout_link = QVBoxLayout(self.groupBox_link)
        self.verticalLayout_link.setSpacing(11)
        self.verticalLayout_link.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_link.setObjectName(u"verticalLayout_link")

        # 4.【路段处理的功能分组】的标题
        self.horizontalLayout_link_title = QHBoxLayout()
        # 文本框
        self.label_link_title = QLabel("四、路段处理")
        self.label_link_title.setFont(font_title)
        self.label_link_title.setStyleSheet("color: red;")
        self.horizontalLayout_link_title.addWidget(self.label_link_title)
        # 按钮
        self.btn_link_title_view = QPushButton()
        self.btn_link_title_view.setObjectName(u"btn_link_title_view")
        self.btn_link_title_view.setFixedWidth(90)
        self.horizontalLayout_link_title.addWidget(self.btn_link_title_view)
        # 加入垂直布局
        self.verticalLayout_link.addLayout(self.horizontalLayout_link_title)

        # 4.1.【创建路段】的按键
        # 输入框
        self.text_link_create = QLineEdit(self.centralWidget)
        self.text_link_create.setPlaceholderText("x1,y1,z1,x2,y2,z2(,move)")
        self.verticalLayout_link.addWidget(self.text_link_create)
        # 按钮
        self.btn_link_create = QPushButton(self.centralWidget)
        self.btn_link_create.setObjectName(u"btnOutputOpenDrive")
        self.verticalLayout_link.addWidget(self.btn_link_create)

        # 4.2.【打断路段】的按键
        # 输入框
        self.text_link_split = QLineEdit(self.centralWidget)
        self.text_link_split.setPlaceholderText("link_id,x,y;link_id,x,y...")
        self.verticalLayout_link.addWidget(self.text_link_split)
        # 按钮
        self.btn_link_split = QPushButton(self.centralWidget)
        self.btn_link_split.setObjectName(u"btn_link_split")
        self.verticalLayout_link.addWidget(self.btn_link_split)

        # 4.3.【连接路段】的按键
        self.btn_link_join = QPushButton(self.centralWidget)
        self.btn_link_join.setObjectName(u"btn_link_join")
        self.verticalLayout_link.addWidget(self.btn_link_join)

        # 4.4.【简化路段】的按键
        self.btn_link_simplify = QPushButton(self.centralWidget)
        self.btn_link_simplify.setObjectName(u"btn_link_simplify")
        self.verticalLayout_link.addWidget(self.btn_link_simplify)

        # 除了标题之外的组件
        self.group_link = [
            self.text_link_create,
            self.btn_link_create,
            self.text_link_split,
            self.btn_link_split,
            self.btn_link_join,
            self.btn_link_simplify
            ]

        #######################################################################

        # 5.信息窗
        self.centralWidget2 = QWidget()
        self.centralWidget2.setObjectName(u"centralWidget2")
        self.centralWidget2.setFixedWidth(420)

        # 【主窗口】的【布局管理器】
        self.verticalLayout_center2 = QVBoxLayout(self.centralWidget2)
        self.verticalLayout_center2.setSpacing(12)
        self.verticalLayout_center2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_center2.setObjectName(u"verticalLayout_center")

        # 【信息窗】的界面
        self.groupBox_info = QGroupBox()
        self.groupBox_info.setObjectName(u"groupBox")
        # self.verticalLayout_center.addWidget(self.groupBox_info)
        self.verticalLayout_center2.addWidget(self.groupBox_info)

        # 【信息窗】的布局管理器
        self.verticalLayout_info = QVBoxLayout(self.groupBox_info)
        self.verticalLayout_info.setSpacing(6)
        self.verticalLayout_info.setObjectName(u"verticalLayout_info")
        self.verticalLayout_info.setContentsMargins(1, 1, 1, 1)

        # 【信息窗】的【文本框】
        self.txt_message = QTextBrowser(self.groupBox_info)
        self.txt_message.setObjectName(u"txt_message")
        self.verticalLayout_info.addWidget(self.txt_message)

        #######################################################################

        # 设置名称
        self.retranslateUi(MyUIAPI_Class)
        QMetaObject.connectSlotsByName(MyUIAPI_Class)


    def retranslateUi(self, MyUIAPI_Class):
        MyUIAPI_Class.setWindowTitle(QCoreApplication.translate("MyUIAPI_Class", u"TESS_API_EXAMPLE", None))

        # 设置字体
        self.groupBox_input.setFont(font_content)
        self.groupBox_output.setFont(font_content)
        self.groupBox_traj.setFont(font_content)
        self.groupBox_link.setFont(font_content)

        # 按键
        # 〇、锦上添花
        self.btn_input_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
        self.btn_output_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
        self.btn_traj_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
        self.btn_link_title_view.setText(QCoreApplication.translate("MyUIAPI_Class", '收起▼', None))
        # 一、导入
        self.btn_input_excel.setText(QCoreApplication.translate("MyUIAPI_Class", 'import Excel (*.xlsx/*.csv)', None))
        self.btn_input_opendrive.setText(QCoreApplication.translate("MyUIAPI_Class", 'import OpenDrive (*.xodr)', None))
        self.btn_input_shape.setText(QCoreApplication.translate("MyUIAPI_Class", 'import Shapefile (*.shp)', None))
        self.btn_input_osm.setText(QCoreApplication.translate("MyUIAPI_Class", 'import OpenStreetMap (by osm API)', None))
        # 二、导出
        self.btn_output_opendrive.setText(QCoreApplication.translate("MyUIAPI_Class", 'export OpenDrive (*.xodr)', None))
        self.btn_output_shape.setText(QCoreApplication.translate("MyUIAPI_Class", 'export Shapefile (*.shp)', None))
        self.btn_output_geojson.setText(QCoreApplication.translate("MyUIAPI_Class", 'export GeoJson (*.geojson)', None))
        self.btn_output_unity.setText(QCoreApplication.translate("MyUIAPI_Class", 'export Unity (*.json)', None))
        self.btn_output_json.setText(QCoreApplication.translate("MyUIAPI_Class", 'export Json (*.json)', None))
        # 三、轨迹
        self.btn_traj_viewTrajPath.setText(QCoreApplication.translate("MyUIAPI_Class", '查看保存地址', None))
        self.btn_traj_changeTrajPath.setText(QCoreApplication.translate("MyUIAPI_Class", '更改保存地址', None))
        # 四、路段
        self.btn_link_create.setText(QCoreApplication.translate("MyUIAPI_Class", '创 建 路 段', None))
        self.btn_link_split.setText(QCoreApplication.translate("MyUIAPI_Class", '打 断 路 段', None))
        self.btn_link_join.setText(QCoreApplication.translate("MyUIAPI_Class", '连 接 全 部 路 段', None))
        self.btn_link_simplify.setText(QCoreApplication.translate("MyUIAPI_Class", '简 化 路 网', None))


