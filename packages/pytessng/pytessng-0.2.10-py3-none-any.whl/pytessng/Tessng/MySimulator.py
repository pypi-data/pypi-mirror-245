from PySide2.QtCore import QObject, Signal
import os
import sys
import json
import ipaddress
from datetime import datetime
from pyproj import Proj

from DLLs.Tessng import PyCustomerSimulator, tessngIFace, p2m
from Toolbox.traj_output.traj_output import get_traj_data
from Toolbox.traj_output.kafka_producer import KafkaMessageProducer, kafka_send_message

class MySimulator(QObject, PyCustomerSimulator):
    signalRunInfo = Signal(str)
    forStopSimu = Signal()
    forReStartSimu = Signal()

    def __init__(self):
        QObject.__init__(self)
        PyCustomerSimulator.__init__(self)

        # 保存为json
        self.state_exportJson = sys.modules["__main__"].__dict__["state_exportJson"]
        # 保存json路径
        self.json_save_path = None # str

        # 是否上传至kafka
        self.state_exportKafka = sys.modules["__main__"].__dict__["state_exportKafka"]
        # 上传kafka位置
        self.kafka_producer = None

        # 投影
        self.proj = None

        # 提示窗函数
        self.showInfoBox = sys.modules["__main__"].__dict__["function_showInfoBox"]

    # 仿真开始之前
    def ref_beforeStart(self, ref_keepOn):
        iface = tessngIFace()
        simuiface = iface.simuInterface()
        # # 设置仿真精度
        # simuiface.setSimuAccuracy(5)

        # 可在此设置本次仿真参数
        ref_keepOn.value = True

        # 设置保存至json路径
        self.set_json()
        # 设置上传至kafka路径
        self.set_kafka("before_simu")
        # 设置投影
        self.set_proj("before_simu")

    def afterStop(self):
        # 设置kafka
        self.set_kafka("after_simu")
        # 设置投影
        self.set_proj("after_simu")

    def afterOneStep(self):
        iface = tessngIFace()
        simuiface = iface.simuInterface()

        # 如果不需要导出，就不需要计算
        if not self.state_exportJson.isChecked() and not self.state_exportKafka.isChecked():
            return

        # 轨迹数据计算和导出
        traj_data = get_traj_data(simuiface, self.proj, p2m)

        # 需要保存为json
        if self.state_exportJson.isChecked():
            # 当前仿真计算批次
            batchNum = simuiface.batchNumber()
            file_path = self.json_save_path.format(batchNum)
            # 将JSON数据写入文件
            with open(file_path, 'w') as file:
                file.write(json.dumps(traj_data, indent=4))

        # 需要上传至kafka
        if self.state_exportKafka.isChecked():
            if self.kafka_producer:
                # 使用线程来发送，不会阻塞主进程，但不知道是否发送成功
                kafka_send_message(self.kafka_producer, traj_data)

        # # 信息窗格信息
        # strVehiCount = str(len(lAllVehi))
        # strSimuTime = str(simuTime)
        # runInfo = f"运行车辆数：{strVehiCount}\n仿真时间：{strSimuTime}(毫秒)"
        # self.signalRunInfo.emit(runInfo)

    # 设置保存为json的路径
    def set_json(self,):
        # 文件夹名称
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S")
        folder_path = os.path.join(sys.modules["__main__"].__dict__['location_exportJson'], f"标准格式车辆轨迹_{formatted_time}")
        print(folder_path)

        # 创建文件夹
        try:
            os.makedirs(folder_path)
        except FileExistsError:
            print(f"文件夹'{folder_path}'已经存在，无需创建")

        self.json_save_path = os.path.join(folder_path, "{}.json")

    # 设置上传至kafka的路径
    def set_kafka(self, mode):
        location_exportKafka = sys.modules["__main__"].__dict__["location_exportKafka"]
        IP_Qline = location_exportKafka["IP"]
        port_Qline = location_exportKafka["port"]
        topic_Qline = location_exportKafka["topic"]

        if mode == "before_simu":
            if not self.state_exportKafka.isChecked():
                self.state_exportKafka.setEnabled(False)
                return

            # 把按钮设为只读
            IP_Qline.setReadOnly(True)
            port_Qline.setReadOnly(True)
            topic_Qline.setReadOnly(True)

            # kafka的IP/port和topic
            IP = IP_Qline.text()
            port = port_Qline.text()
            topic = topic_Qline.text()

            # 对IP、端口号、topic进行核验
            if not IP:
                self.state_exportKafka.setChecked(False)
                self.state_exportKafka.setEnabled(False)
                self.showInfoBox("未有输入IPv4地址！", "warning")
                return
            if not port:
                self.state_exportKafka.setChecked(False)
                self.state_exportKafka.setEnabled(False)
                self.showInfoBox("未有输入端口号！", "warning")
                return
            if not topic:
                self.state_exportKafka.setChecked(False)
                self.state_exportKafka.setEnabled(False)
                self.showInfoBox("未有输入topic！", "warning")
                return
            try:
                ipaddress.ip_address(IP)
            except:
                self.state_exportKafka.setChecked(False)
                self.state_exportKafka.setEnabled(False)
                self.showInfoBox("未有输入正确的IPv4地址！", "warning")
                return
            try:
                float(port)
            except:
                self.state_exportKafka.setChecked(False)
                self.state_exportKafka.setEnabled(False)
                self.showInfoBox("未有输入正确的端口号！", "warning")
                return

            # kafka对象
            server_path = f"{IP}:{port}"
            try:
                self.kafka_producer = KafkaMessageProducer(server_path, topic)
                print("kafka连接成功！")
            except:
                pass

        elif mode == "after_simu":
            self.state_exportKafka.setEnabled(True)
            # 把按钮只读取消
            IP_Qline.setReadOnly(False)
            port_Qline.setReadOnly(False)
            topic_Qline.setReadOnly(False)

            # kafka对象关闭
            try:
                self.kafka_producer.close()
            except:
                pass

    # 设置投影
    def set_proj(self, mode):
        lon_Qline = sys.modules["__main__"].__dict__['lon_and_lat']["lon"]
        lat_Qline = sys.modules["__main__"].__dict__['lon_and_lat']["lat"]

        if mode == "before_simu":
            # 把按钮设为只读
            lon_Qline.setReadOnly(True)
            lat_Qline.setReadOnly(True)

            try:
                lon = float(lon_Qline.text())
                lat = float(lat_Qline.text())
                if not (-180<lon<180) or not (-90<lat<90):
                    self.proj = None
                    return
                # 轨迹转换的投影
                self.proj = Proj(f'+proj=tmerc +lat_0={lat} +lon_0={lon} +k=1 +ellps=WGS84 +units=m +no_defs')
            except Exception as e:
                self.proj = None
                # print(str(e))

        elif mode == "after_simu":
            # 把按钮只读取消
            lon_Qline.setReadOnly(False)
            lat_Qline.setReadOnly(False)

        else:
            pass

