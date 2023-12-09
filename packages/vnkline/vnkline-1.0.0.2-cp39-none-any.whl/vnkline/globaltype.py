from ctypes import *


class VNInstrument(Structure):
    _fields_ = [('InstrumentID', c_char * 81)]
    pass


class KLineDataType(Structure):
    _fields_ = [('Open', c_double),
                ('High', c_double),
                ('Low', c_double),
                ('Close', c_double),
                ('KlineTime', c_double),
                ('Volume', c_int),
                ('Minutes', c_int),
                ('InstrumentID', c_char * 81),
                ('TradingDay', c_char * 9)
                ]
