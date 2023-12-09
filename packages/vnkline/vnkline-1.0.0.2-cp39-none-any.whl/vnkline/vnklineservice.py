# -*- coding=utf-8 -*-
# 官方网站：http://www.vnpy.cn
from globaltype import *
import os.path
import threading

class vnklineservice(object):
    def __init__(self, signal_td):
        self.signal_td = signal_td
        currpath = os.path.abspath(os.path.dirname(__file__))
        self.vnkline = CDLL(currpath + '\\vnklineservice.dll')

        self.fGetServerKline = self.vnkline.GetServerKline
        self.fGetServerKline.argtypes = [c_void_p, c_int32]
        self.fGetServerKline.restype = c_int32

        self.fGetServerMultiKline = self.vnkline.GetServerMultiKline
        self.fGetServerMultiKline.argtypes = [c_void_p, c_int32, c_int32, c_void_p]
        self.fGetServerMultiKline.restype = c_int32

        self.fGetTradingDay = self.vnkline.GetTradingDay
        self.fGetTradingDay.argtypes = []
        self.fGetTradingDay.restype = c_int32

    def GetServerKline(self, InstrumentID, TradeingDay):
        try:
            thisInstrumentID = VNInstrument()
            thisInstrumentID.InstrumentID = bytes(InstrumentID, encoding="utf-8")
            # self.fGetServerKline(byref(thisInstrumentID), TradeingDay)
            t1 = threading.Thread(target=self.fGetServerKline, args=(byref(thisInstrumentID), TradeingDay,))
            t1.start()
            t1.join()
            return 1
        except Exception as e:
            print("GetKline Error:" + repr(e))
            return 0


    def GetTradingDay(self):
        try:
            return self.fGetTradingDay()
        except Exception as e:
            print("GetTradingDay Error:" + repr(e))
            return -1

    # 注册行情回调
    def VNRegOnKline(self):
        CMPFUNC = CFUNCTYPE(None, POINTER(KLineDataType))
        self.vnkline.VNRegOnKline(CMPFUNC(self.OnKline))
