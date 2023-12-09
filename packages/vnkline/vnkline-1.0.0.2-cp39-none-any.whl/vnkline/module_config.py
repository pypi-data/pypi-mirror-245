from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
import time
import globalvar
import configparser
from globaltype import *

instrumenttableid = 0

VN_MOUTHNUM = 12


def update_instrument(instrumentID, instrumentName, exchange, jump):
    global instrumenttableid
    row_cnt = globalvar.ui.table_instrument.rowCount()
    thiskey = str(instrumentID)
    if instrumentID == '':
        return
    if thiskey in globalvar.dict_position:
        thisrowid = row_cnt
        pass
    else:
        globalvar.dict_position[thiskey] = row_cnt
        globalvar.ui.table_instrument.insertRow(row_cnt)  # 尾部插入一行新行表格
        thisrowid = row_cnt
    column_cnt = globalvar.ui.table_instrument.columnCount()  # 返回当前列数
    # item = QTableWidgetItem(str(instrumentID, encoding="utf-8"))

    thisInstrumentID = VNInstrument()
    thisInstrumentID.InstrumentID = bytes(instrumentID, 'gb2312')

    instrumenttableid = instrumenttableid + 1
    item = QTableWidgetItem(str(instrumenttableid))
    globalvar.ui.table_instrument.setItem(thisrowid, 0, item)
    item = QTableWidgetItem(str(instrumentName))
    globalvar.ui.table_instrument.setItem(thisrowid, 1, item)
    item = QTableWidgetItem(instrumentID)
    globalvar.ui.table_instrument.setItem(thisrowid, 2, item)
    item = QTableWidgetItem(str(exchange))
    globalvar.ui.table_instrument.setItem(thisrowid, 3, item)
    item = QTableWidgetItem("%s" % jump)
    globalvar.ui.table_instrument.setItem(thisrowid, 4, item)


# MyReadConfig读取配置文件，初始化选项
class MyReadConfig(QtCore.QThread):
    global list_INE, list_CFFEX, list_SHFE, list_DCE, list_CZCE
    global dict_exchange, dict_instrument

    def __init__(self):
        super().__init__()

    savedate = 0
    thisdate = 0

    def mounthyear4(self, thisdate, add):
        year = (int)(thisdate * 0.01)
        mounth = thisdate - year * 100
        mounth = mounth + add
        if mounth > 12:
            mounth = mounth - 12
            year = year + 1
        thisdate = year * 100 + mounth
        return thisdate

    def mounthyear3(self, thisdate, add):
        year = (int)(thisdate * 0.01)
        y = (int)(thisdate * 0.001)
        mounth = thisdate - year * 100
        mounth = mounth + add
        if mounth > 12:
            mounth = mounth - 12
            year = year + 1
        thisdate = year * 100 + mounth
        thisdate = thisdate - 1000 * y
        return thisdate

    def UpdateMainType(self, instrumentMain, instrumentName, exchange, jump):
        global tempdate
        returnvalue = 0
        savedate = time.strftime("%Y%m%d", time.localtime())
        tvs = (int(float(savedate) * 0.000001)) * 1000000
        tempdate = int((float(savedate) - float(tvs)) * 0.01)
        tj = 0
        for j in range(VN_MOUTHNUM):
            if exchange == 'INE':
                returnvalue = self.mounthyear4(tempdate, j)
                update_instrument(instrumentMain + str(returnvalue), instrumentName, exchange, jump)
                # globalvar.md.SubscribeMarketData(instrumentMain + str(returnvalue))
                if j == 0:
                    if len(instrumentMain) > 0:
                        globalvar.set_list_INE(instrumentMain + ',' + instrumentName + ',' + exchange)
                globalvar.dict_exchange[instrumentMain + str(returnvalue)] = exchange + ',能源所'
                globalvar.dict_instrument[
                    instrumentMain + str(returnvalue)] = instrumentMain + ',' + instrumentName + ',' + exchange
            elif exchange == 'CFFEX':
                returnvalue = self.mounthyear4(tempdate, j)
                update_instrument(instrumentMain + str(returnvalue), instrumentName, exchange, jump)

                # globalvar.md.SubscribeMarketData(instrumentMain + str(returnvalue))
                if j == 0:
                    if len(instrumentMain) > 0:
                        globalvar.set_list_CFFEX(instrumentMain + ',' + instrumentName + ',' + exchange)
                globalvar.dict_exchange[instrumentMain + str(returnvalue)] = exchange + ',中金所'
                globalvar.dict_instrument[
                    instrumentMain + str(returnvalue)] = instrumentMain + ',' + instrumentName + ',' + exchange
            elif exchange == 'SHFE':
                returnvalue = self.mounthyear4(tempdate, j)
                update_instrument(instrumentMain + str(returnvalue), instrumentName, exchange, jump)
                # globalvar.md.SubscribeMarketData(instrumentMain + str(returnvalue))
                if j == 0:
                    if len(instrumentMain) > 0:
                        globalvar.set_list_SHFE(instrumentMain + ',' + instrumentName + ',' + exchange)
                globalvar.dict_exchange[instrumentMain + str(returnvalue)] = exchange + ',上期所'
                globalvar.dict_instrument[
                    instrumentMain + str(returnvalue)] = instrumentMain + ',' + instrumentName + ',' + exchange
            elif exchange == 'DCE':
                returnvalue = self.mounthyear4(tempdate, j)
                update_instrument(instrumentMain + str(returnvalue), instrumentName, exchange, jump)
                # globalvar.md.SubscribeMarketData(instrumentMain + str(returnvalue))
                if j == 0:
                    if len(instrumentMain) > 0:
                        globalvar.set_list_DCE(instrumentMain + ',' + instrumentName + ',' + exchange)
                globalvar.dict_exchange[instrumentMain + str(returnvalue)] = exchange + ',大商所'
                globalvar.dict_instrument[
                    instrumentMain + str(returnvalue)] = instrumentMain + ',' + instrumentName + ',' + exchange
            elif exchange == 'CZCE':
                returnvalue = self.mounthyear3(tempdate, j)
                update_instrument(instrumentMain + str(returnvalue), instrumentName, exchange, jump)

                # print('test: '+instrumentMain + str(returnvalue))
                # globalvar.md.SubscribeMarketData(instrumentMain + str(returnvalue))
                if j == 0:
                    if len(instrumentMain) > 0:
                        globalvar.set_list_CZCE(instrumentMain + ',' + instrumentName + ',' + exchange)
                globalvar.dict_exchange[instrumentMain + str(returnvalue)] = exchange + ',郑商所'
                globalvar.dict_instrument[
                    instrumentMain + str(returnvalue)] = instrumentMain + ',' + instrumentName + ',' + exchange
        return returnvalue

    # 生成合约列表
    def generateinstrumentID(self):
        instrumentidlist = []
        with open('InstrumentID.ini', 'r') as f:
            for line in f:
                instrumentIDarr = line.strip('\n').split(',')
                instrumentidlist.append(list(line.strip('\n').split(',')))
                self.UpdateMainType(instrumentIDarr[1], instrumentIDarr[2], instrumentIDarr[3],
                                    instrumentIDarr[4])  # test

        # globalvar.printlist()
        # print("输出list: " + globalvar.list_INE[-1])
        globalvar.ui.callback_md_combox()

    # 读取配置文件
    def readklineserversetting(self):
        try:
            global config
            config = configparser.ConfigParser()
            # -read读取ini文件
            config.read('global.ini', encoding='utf-8')
            # 是否从K线服务器读取读取当日数据
            globalvar.klineserverstate = config.getint('setting', 'klineserverstate')
            if globalvar.klineserverstate == 0:
                globalvar.ui.Button_KlineSource_RealTimeTick.setChecked(True)
                globalvar.ui.Button_KlineSource_ServerToday.setChecked(False)
            else:
                globalvar.ui.Button_KlineSource_RealTimeTick.setChecked(False)
                globalvar.ui.Button_KlineSource_ServerToday.setChecked(True)


        except Exception as e:
            print("readklineserversetting Error:" + repr(e))

    # 读取股票图表访问历史列表
    def readhistorystock(self):
        with open('historystock.ini', 'r') as f:
            for line in f:
                historystocklist = line.strip('\n').split(',')
                for i in range(min(len(globalvar.ui.Button_h), len(historystocklist))):
                    globalvar.ui.Button_h[i].setText(str(historystocklist[i]))
                    if len(historystocklist) > VN_MOUTHNUM:
                        hstr = ''
                        les = min(VN_MOUTHNUM, len(historystocklist))
                        for j in range(les):
                            if j < les - 1:
                                hstr = hstr + historystocklist[j] + ','
                            else:
                                hstr = hstr + historystocklist[j]
                        with open("historystock.ini", "w") as f:
                            f.write(hstr)

    def updatehistorystockagain(self, instrument, historystocklist2):
        tempinstrument = instrument
        if tempinstrument.strip('0123456789') == instrument:
            return
        reagain = 0
        if instrument in historystocklist2:
            for i in range(len(historystocklist2)):
                print(historystocklist2)
                if str(historystocklist2[i]) == instrument:
                    historystocklist2.pop(i)
                    reagain = 1
                    break
        if reagain == 1:
            self.updatehistorystockagain(instrument, historystocklist2)
        else:
            historystocklist2.insert(0, instrument)
            hstr = ''
            les = len(historystocklist2)
            for i in range(les):
                if i < les - 1:
                    hstr = hstr + historystocklist2[i] + ','
                else:
                    hstr = hstr + historystocklist2[i]
            with open("historystock.ini", "w") as f:
                f.write(hstr)
        self.readhistorystock()

    def updatehistorystock(self, instrument):
        tempinstrument = instrument
        if tempinstrument.strip('0123456789') == instrument:
            return
        reagain = 0
        with open('historystock.ini', 'r') as f:
            for line in f:
                historystocklist = line.strip('\n').split(',')
                if instrument in historystocklist:
                    for i in range(len(historystocklist)):
                        if str(historystocklist[i]) == instrument:
                            historystocklist.pop(i)
                            reagain = 1
                            break
        if reagain == 1:
            self.updatehistorystockagain(instrument, historystocklist)
        else:
            historystocklist.insert(0, instrument)
            hstr = ''
            les = len(historystocklist)
            for i in range(les):
                if i < les - 1:
                    hstr = hstr + historystocklist[i] + ','
                else:
                    hstr = hstr + historystocklist[i]
            with open("historystock.ini", "w") as f:
                f.write(hstr)
        self.readhistorystock()
