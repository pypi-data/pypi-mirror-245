from typing import Tuple

from .req_rsp import ReqRspDict, ReqRsp
from ..listener import IListener
from ..interface import IData, MsgID
from ..tsocket import TSocket
from ..data.MessageData import MessageData
from ..data.market.TickData import TickData
from ..data.market.OHLCData import OHLCData
from ..data.market.MarketParamData import MarketParamData
from ..data.market.HistoryOHLCParamData import HistoryOHLCParamData
from ..data.market.SubOHLCParamData import SubOHLCParamData
from ..data.market.QueryParamData import QueryParamData
from ..data.market.SaveOHLCListParamData import SaveOHLCListParamData
import pandas as pd


class MarketHandle():
    __ReqID: int = 0
    __Listener: IListener = None
    __ReqRspDict: ReqRspDict = ReqRspDict()

    def __init__(self, tsocket: TSocket):
        self.__TSocket = tsocket
        self.__TSocket.set_market_callback(self.__recv_msg)

    def set_callback(self, **kwargs):
        if kwargs is None:
            return
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def set_listener(self, listener: IListener):
        self.__Listener = listener

    def set_market_params(self, params: MarketParamData) -> Tuple[bool, str]:
        return self.__wait_send_msg(int(MsgID.MSGID_Market_SetParams.value), params)

    def subscribe(self, params: QueryParamData) -> Tuple[bool, str]:
        return self.__wait_send_msg(int(MsgID.MSGID_Market_Sub.value), params)

    def subscribe_ohlc(self, params: SubOHLCParamData) -> Tuple[bool, str]:
        return self.__wait_send_msg(int(MsgID.MSGID_Market_SubOHLC.value), params)

    def save_ohlc_list(self, params: SaveOHLCListParamData) -> Tuple[bool, str]:
        return self.__wait_send_msg(int(MsgID.MSGID_Market_SaveOHLCList.value), params)

    def get_history_ohlc(self, params: HistoryOHLCParamData) -> Tuple[bool, str, pd.DataFrame]:
        self.__ReqID = self.__ReqID + 1
        mid = int(MsgID.MSGID_Market_GetHistoryOHLC.value)
        msg = MessageData(mid=mid, request_id=self.__ReqID)
        if params is not None:
            msg.UData = params.pack()

        key = '%s_%s' % (mid, self.__ReqID)
        req_rsp = self.__ReqRspDict.new_reqrsp(key, msg)
        if self.__TSocket.send_message(msg) is False:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令失败', None]

        rsp = req_rsp.wait_last_rsp(10)
        if rsp is None:
            self.__ReqRspDict.remove(key)
            return [False, '获取历史OHLC数据超时', None]

        if params.IsReturnList is True:
            return [True, '获取历史OHLC数据成功', self.__unpack_ohlc_list(req_rsp)]
        else:
            return [True, '获取历史OHLC数据成功', self.__unpack_ohlc_dataframe(req_rsp)]

    def __notify_on_tick(self, msg: MessageData):
        hasontick = hasattr(self, 'on_tick')
        if hasontick is False and self.__Listener is None:
            print('未定义任何on_tick回调方法')
            return
        t = TickData()
        if t.un_pack(msg.UData) is True:
            if hasontick is True:
                self.on_tick(t)
            if self.__Listener is not None:
                self.__Listener.on_tick(t)

    def __notify_on_ohlc(self, msg: MessageData):
        hasonohlc = hasattr(self, 'on_ohlc')
        if hasonohlc is False and self.__Listener is None:
            print('未定义任何on_ohlc回调方法')
            return
        o = OHLCData()
        if o.un_pack(msg.UData) is True:
            if hasonohlc is True:
                self.on_ohlc(o)
            if self.__Listener is not None:
                self.__Listener.on_ohlc(o)

    def __unpack_ohlc_list(self, reqrsp: ReqRsp):
        ohlcs = list()
        rsp_list = reqrsp.get_rsp_list()
        for r in rsp_list:
            if len(r.UData) > 0:
                rspparams = HistoryOHLCParamData()
                rspparams.un_pack(r.UData)
                for ot in rspparams.OHLCList:
                    o = OHLCData()
                    o.tuple_to_obj(ot)
                    ohlcs.append(o)
        return ohlcs

    def __unpack_ohlc_dataframe(self, reqrsp: ReqRsp):
        dfrtn = pd.DataFrame()
        rsp_list = reqrsp.get_rsp_list()
        for r in rsp_list:
            if len(r.UData) > 0:
                rspparams = HistoryOHLCParamData()
                rspparams.un_pack(r.UData)
                df = pd.DataFrame(rspparams.OHLCList, columns=['ExchangeID', 'InstrumentID', 'TradingDay', 'TradingTime', 'StartTime', 'EndTime', 'ActionDay',
                                                               'ActionTimeSpan', 'Range', 'Index', 'OpenPrice', 'HighestPrice', 'LowestPrice', 'ClosePrice',
                                                               'TotalTurnover', 'TotalVolume', 'OpenInterest', 'PreSettlementPrice', 'ChangeRate', 'ChangeValue',
                                                               'OpenBidPrice', 'OpenAskPrice', 'OpenBidVolume', 'OpenAskVolume', 'HighestBidPrice', 'HighestAskPrice',
                                                               'HighestBidVolume', 'HighestAskVolume', 'LowestBidPrice', 'LowestAskPrice', 'LowestBidVolume', 'LowestAskVolume',
                                                               'CloseBidPrice', 'CloseAskPrice', 'CloseBidVolume', 'CloseAskVolume'])
                dfrtn = pd.concat([dfrtn, df], ignore_index=True, copy=False)
        return dfrtn

    def __recv_msg(self, msg: MessageData):
        if msg.MID == int(MsgID.MSGID_Market_Tick.value):
            self.__notify_on_tick(msg)
            return
        elif msg.MID == int(MsgID.MSGID_Market_OHLC.value):
            self.__notify_on_ohlc(msg)
            return

        key = '%s_%s' % (msg.MID, msg.RequestID)
        reqrsp: ReqRsp = self.__ReqRspDict.get_reqrsp(key)
        if reqrsp is not None:
            reqrsp.append_rsp(msg)

    def __wait_send_msg(self, mid, params: IData):
        self.__ReqID = self.__ReqID + 1
        msg = MessageData(mid=mid, request_id=self.__ReqID)
        if params is not None:
            msg.UData = params.pack()

        key = '%s_%s' % (mid, self.__ReqID)

        req_rsp = self.__ReqRspDict.new_reqrsp(key, msg)
        if self.__TSocket.send_message(msg) is False:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令失败']

        rsp = req_rsp.wait_last_rsp(10)
        if rsp is None:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令超时']
        return [rsp.RspSuccess, rsp.RspMsg]
