# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from PySide2.QtWidgets import QApplication

from DLLs.Tessng import TessngFactory
from Tessng.MyPlugin import MyPlugin


class MyTessngApp:
    def __init__(self, ):
        self.app = QApplication()
        self.workspace = os.path.join(os.fspath(Path(__file__).resolve().parent), "WorkSpace")
        self.config = {
            '__workspace': self.workspace,
            '__simuafterload': False,
            '__custsimubysteps': False,
            '__allowspopup': False,
        }
        self.plugin = MyPlugin()
        self.factory = TessngFactory()
        self.tessng = self.factory.build(self.plugin, self.config)

    def run(self, ):
        if self.tessng is not None:
            sys.exit(self.app.exec_())
        else:
            sys.exit()


if __name__ == '__main__':
    my_app = MyTessngApp()
    my_app.run()

