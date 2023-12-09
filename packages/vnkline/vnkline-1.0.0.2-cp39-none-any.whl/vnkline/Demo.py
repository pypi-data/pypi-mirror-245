# 官方网站：http://www.vnpy.cn
import logging
import os
import sys
import time
from os.path import abspath, dirname
import qdarkstyle
import ui.example_pyqt5_ui as example_ui
import module_config
import module_kline
from PyQt5 import QtWidgets, QtCore
import globalvar
import threading
globalvar._init()
sys.path.insert(0, abspath(dirname(abspath(__file__)) + '/..'))
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
globalvar.ui = example_ui.Ui_MainWindow()


def InitReadConfig():
    globalvar.rc = module_config.MyReadConfig()
    globalvar.rc.ui = globalvar.ui
    try:
        globalvar.rc.generateinstrumentID()  # test
    except Exception as e:
        print("generateinstrumentID Error:" + repr(e))

    globalvar.rc.readklineserversetting()
    globalvar.rc.readhistorystock()
    globalvar.ui.Function_Buttonclickh1()


def main():
    globalvar.currpath = os.path.abspath(os.path.dirname(__file__))
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    globalvar.ui.setupUi(window)
    item = QtWidgets.QTableWidgetItem("1")
    item.setCheckState(QtCore.Qt.Unchecked)
    window.setWindowTitle("VNPY官方 (http://www.vnpy.cn) K线服务模块")
    globalvar.ui.dockWidget1.raise_()
    print(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    if "--travis" in sys.argv:
        QtCore.QTimer.singleShot(2000, app.exit)
    window.setFixedSize(1366, 740)
    #window.showMaximized()
    window.show()

    time.sleep(2)
    globalvar.vk = module_kline.MyKlineService(globalvar.ui.callback_kline)
    globalvar.vk.ui = globalvar.ui
    InitReadConfig()

    app.exec_()
    os._exit(1)


if __name__ == "__main__":
    main()
