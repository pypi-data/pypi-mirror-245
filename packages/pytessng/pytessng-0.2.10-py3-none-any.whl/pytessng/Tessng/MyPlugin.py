from PySide2.QtWidgets import QDockWidget, QMenu
from PySide2.QtCore import Qt
import webbrowser
from functools import partial

from DLLs.Tessng import TessPlugin, tessngIFace
from Tessng.MyUIAPI import MyUIAPI
from Tessng.MyNet import MyNet
from Tessng.MySimulator import MySimulator


# 用户插件，继承自TessPlugin
class MyPlugin(TessPlugin):
    def __init__(self):
        super(MyPlugin, self).__init__()
        self.mNetInf = None
        self.mSimuInf = None

    def initGui(self):
        iface = tessngIFace()
        win = iface.guiInterface().mainWindow()

        self.examleWindow = MyUIAPI()
        
        # 在TESS NG主界面上增加 QDockWidget对象
        # 左侧界面
        dockWidget_left = QDockWidget("操作面板", win)
        dockWidget_left.setObjectName("mainDockWidget")
        dockWidget_left.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dockWidget_left.setAllowedAreas(Qt.LeftDockWidgetArea)
        dockWidget_left.setWidget(self.examleWindow.centralWidget())
        iface.guiInterface().addDockWidgetToMainWindow(Qt.DockWidgetArea(1), dockWidget_left)
        
        # 右侧界面
        dockWidget_right = QDockWidget("信息面板", win)
        dockWidget_right.setObjectName("mainDockWidget2")
        dockWidget_right.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dockWidget_right.setAllowedAreas(Qt.RightDockWidgetArea)
        dockWidget_right.setWidget(self.examleWindow.ui.centralWidget2)
        iface.guiInterface().addDockWidgetToMainWindow(Qt.DockWidgetArea(2), dockWidget_right)

        # 增加菜单及菜单项
        menuBar = iface.guiInterface().menuBar()
        menu = QMenu(menuBar)
        menu.setObjectName("说明书")
        menuBar.addAction(menu.menuAction())
        menu.setTitle("说明书")
        # 1
        action_1 = menu.addAction("TESSNG说明书")
        action_1.triggered.connect(partial(self.open_instruction, "WorkSpace\\Doc\\TESSNG 微观交通仿真软件用户使用说明书 V3.1.pdf"))
        # 2
        action_2 = menu.addAction("TESSNG Python API说明书")
        action_2.triggered.connect(partial(self.open_instruction, "WorkSpace\\Doc\\TESSNG 二次开发Python API使用说明书 V2.1.pdf"))
        # 3
        action_3 = menu.addAction("PyTessng说明书")
        action_3.triggered.connect(partial(self.open_instruction, "WorkSpace\\Doc\\PyTessng 说明书 V1.0.pdf"))

    # 过载父类方法，在 TESS NG工厂类创建TESS NG对象时调用
    def init(self):
        self.initGui()
        self.mNetInf = MyNet()
        self.mSimuInf = MySimulator()

        # self.mSimuInf.signalRunInfo.connect(self.examleWindow.showRunInfo)
        # iface = tessngIFace()
        # win = iface.guiInterface().mainWindow()
        # #将信号mSimuInf.forReStopSimu关联到主窗体的槽函数doStopSimu，可以借安全地停止仿真运行
        # self.mSimuInf.forStopSimu.connect(win.doStopSimu, Qt.QueuedConnection)
        # #将信号mSimuInf.forReStartSimu关联到主窗体的槽函数doStartSimu，可以借此实现自动重复仿真
        # self.mSimuInf.forReStartSimu.connect(win.doStartSimu, Qt.QueuedConnection)

    # 过载父类方法，返回插件路网子接口，此方法由TESS NG调用
    def customerNet(self):
        return self.mNetInf

    #过载父类方法，返回插件仿真子接口，此方法由TESS NG调用
    def customerSimulator(self):
        return self.mSimuInf

    def open_instruction(self, pdf_file_path):
        webbrowser.open(pdf_file_path, new=2)
