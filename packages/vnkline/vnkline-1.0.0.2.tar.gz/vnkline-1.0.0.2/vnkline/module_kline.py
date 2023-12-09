from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
# K线数据服务库
from vnklineservice import *
import globalvar


# MyKlineService类继承自vnklineservice类
class MyKlineService(vnklineservice, QtCore.QThread):
    def __init__(self, _signal):
        self._signal = _signal
        super().__init__(_signal)

    # 合约订阅回调
    def OnKline(self, a):
        print(u'从服务器获取K线成功OnKline' + a.contents.InstrumentID)
        globalvar.ui.log_todaymd('从服务器获取K线成功OnKline' + a.contents.InstrumentID)
    '''
    def GetKline(self, InstrumentID, ID):
        vnklineservice().GetKline(InstrumentID.encode('gb2312'), ID)
        return 1
    '''


# 实时数据来自CTP API接口，但CTP不提供历史K线数据，历史K线数据服务是实时K线服务，提供当日M1 K线数据
# 所以K线数据服务端必须闭源，这是选配模块，并不一定要使用，
# 如果想屏蔽本模块（再Main函数删除以下2行
# vk = KLineServiceThread('vk')
# vk.start()）
# 那么VNTrader会根据TICK实时生成M1周期K线
# 回测数据模块、多日K线数据模块正在升级中
class KLineServiceThread(QtCore.QThread):
    signal_getkline = pyqtSignal(str)

    def __del__(self):
        self.wait()

    def __init__(self):
        super(KLineServiceThread, self).__init__()

    def run(self):
        globalvar.vk = MyKlineService(self.signal_getkline)
        globalvar.vk.ui = globalvar.ui
