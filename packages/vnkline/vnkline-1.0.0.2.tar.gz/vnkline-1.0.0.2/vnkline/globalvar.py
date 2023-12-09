# -*- coding: utf-8 -*-
# 本页面用于多个py文件之间共享全局变量
global ui
gui = 0
csvfile = ''
# 屏蔽第一次K线更新
notfirstupdateklineUi = False
dict_position = {}
dict_order = {}
dict_trader = {}
# 只有 data_kline_M1  (M1周期数据)是从服务器获取或实时生成
# 其他周期K线数据是通过Python的Pandas本地合成
# 本地生成数据包括 data_kline_M3、data_kline_M5、data_kline_M10、data_kline_M15、data_kline_M30、data_kline_M60、data_kline_M120、data_kline_D1
# 字段分别为 ID,Data,Time,Open,Close,Low,High
# 调用方式如下
# print("data_kline_M1: " + str(data_kline_M1))
# print("data_kline_M1: " + str(data_kline_M1[0]))
# print("data_kline_M1: " + str(data_kline_M1[1]))
# print("data_kline_M1: " + str(data_kline_M1[2]))
# print("data_kline_M11: " + str(data_kline_M1[2][1]))
# print("data_kline_M12: " + str(data_kline_M1[2][2]))
# 保存订阅的合约的数据， 取值方法 dict_data_kline_M1['ag2110']
dict_dataframe_kline_M1 = {}
dict_dataframe_kline_M3 = {}
dict_dataframe_kline_M5 = {}
dict_dataframe_kline_M10 = {}
dict_dataframe_kline_M15 = {}
dict_dataframe_kline_M30 = {}
dict_dataframe_kline_M60 = {}
dict_dataframe_kline_M120 = {}
dict_dataframe_kline_D1 = {}
# 显示的K线图的个周期数据
data_kline_M1 = []
data_kline_M3 = []
data_kline_M5 = []
data_kline_M10 = []
data_kline_M15 = []
data_kline_M30 = []
data_kline_M60 = []
data_kline_M120 = []
data_kline_D1 = []

# VNPY官方Plus服务账号
global Plus_UserName, Plus_Password
Plus_UserName = "admin"
Plus_Password = "000000"
# 认证用户权限
global PlusAuthState
# K线数据模式，0实时TICK生成K线，1从服务器补齐当日K线，2从服务器补齐多日K线（需Plus会员）
# 用于保存选择框变量
global list_INE, list_CFFEX, list_SHFE, list_DCE, list_CZCE
global dict_exchange, dict_instrument
global thistoday
# 保存当前pygraph K线图、闪电图选中选中合约对应的交易所，合约编码，周期
global selectperiod, selectexchange, selectinstrumenid
# 实例化交易库和行情库作为全局遍历保存
global vk
vk = 0
selectinstrumenid = '1'
selectperiod = 1


def _init():  # 初始化
    global PlusAuthState
    PlusAuthState = 0
    global thistoday
    global vk
    global list_INE, list_CFFEX, list_SHFE, list_DCE, list_CZCE, selectperiod, selectexchange, selectinstrumenid
    list_INE = []
    list_CFFEX = []
    list_SHFE = []
    list_DCE = []
    list_CZCE = []
    global dict_exchange, dict_instrument
    dict_exchange = {}
    dict_instrument = {}


def set_list_INE(value):
    list_INE.append(value)


def get_list_INE(id, defValue=None):
    try:
        return list_INE[id]
    except:
        pass


def getlen_list_INE():
    return len(list_INE)


def set_list_CFFEX(value):
    list_CFFEX.append(value)


def get_list_CFFEX(id, defValue=None):
    try:
        return list_CFFEX[id]
    except:
        pass


def getlen_list_CFFEX():
    return len(list_CFFEX)


def set_list_SHFE(value):
    list_SHFE.append(value)


def get_list_SHFE(id, defValue=None):
    try:
        return list_SHFE[id]
    except:
        pass


def getlen_list_SHFE():
    return len(list_SHFE)


def set_list_DCE(value):
    list_DCE.append(value)


def get_list_DCE(id, defValue=None):
    try:
        return list_DCE[id]
    except:
        pass


def getlen_list_DCE():
    return len(list_DCE)


def set_list_CZCE(value):
    list_CZCE.append(value)


def get_list_CZCE(id, defValue=None):
    try:
        return list_CZCE[id]
    except:
        pass


def getlen_list_CZCE():
    return len(list_CZCE)
