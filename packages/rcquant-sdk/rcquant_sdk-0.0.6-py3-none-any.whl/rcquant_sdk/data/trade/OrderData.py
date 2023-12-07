from ...interface import IData
from ...packer.trade.OrderDataPacker import OrderDataPacker


class OrderData(IData):
    def __init__(self, investorid: str = '', brokerid: str = '', exchangeid: str = '', productid: str = '', producttype: int = 0, instrumentid: str = '', ordertime: str = '', canceltime: str = '',
                 tradingday: str = '', insertdate: str = '', updatetime: str = '', statusmsg: str = '', frontid: int = 0, sessionid: int = 0, orderref: str = '', orderlocalno: str = '',
                 orderid: str = '', relativeordersysid: str = '', brokerorderseq: str = '', price: float = 0.0, stopprice: float = 0.0, volume: int = 0, notradedvolume: int = 0, status: int = 11,
                 direction: int = 1, openclosetype: int = 0, pricecond: int = 1, timecond: int = 3, volumecond: int = 0, hedgetype: int = 0, ordertype: int = 0, actiontype: int = 0,
                 contingentcond: int = 0, frozenmarginprice: float = 0.0, frozenmargin: float = 0.0, frozencommission: float = 0.0, showvolume: int = 0, minvolume: int = 0,
                 priceprecision: int = 0, finbizno: str = '', finalgono: str = '', fininsertlocaltime: int = 0, finrtnorderlocaltime: int = 0, finlockno: str = '',
                 bizname: str = '', rtnorderlocaltime: int = 0):
        super().__init__(OrderDataPacker(self))
        self._InvestorID: str = investorid
        self._BrokerID: str = brokerid
        self._ExchangeID: str = exchangeid
        self._ProductID: str = productid
        self._ProductType: int = producttype
        self._InstrumentID: str = instrumentid
        self._OrderTime: str = ordertime
        self._CancelTime: str = canceltime
        self._TradingDay: str = tradingday
        self._InsertDate: str = insertdate
        self._UpdateTime: str = updatetime
        self._StatusMsg: str = statusmsg
        self._FrontID: int = frontid
        self._SessionID: int = sessionid
        self._OrderRef: str = orderref
        self._OrderLocalNo: str = orderlocalno
        self._OrderID: str = orderid
        self._RelativeOrderSysID: str = relativeordersysid
        self._BrokerOrderSeq: str = brokerorderseq
        self._Price: float = price
        self._StopPrice: float = stopprice
        self._Volume: int = volume
        self._NoTradedVolume: int = notradedvolume
        self._Status: int = status
        self._Direction: int = direction
        self._OpenCloseType: int = openclosetype
        self._PriceCond: int = pricecond
        self._TimeCond: int = timecond
        self._VolumeCond: int = volumecond
        self._HedgeType: int = hedgetype
        self._OrderType: int = ordertype
        self._ActionType: int = actiontype
        self._ContingentCond: int = contingentcond
        self._FrozenMarginPrice: float = frozenmarginprice
        self._FrozenMargin: float = frozenmargin
        self._FrozenCommission: float = frozencommission
        self._ShowVolume: int = showvolume
        self._MinVolume: int = minvolume
        self._PricePrecision: int = priceprecision
        self._FinBizNo: str = finbizno
        self._FinAlgoNo: str = finalgono
        self._FinInsertLocalTime: int = fininsertlocaltime
        self._FinRtnOrderLocalTime: int = finrtnorderlocaltime
        self._FinLockNo: str = finlockno
        self._BizName: str = bizname
        self._RtnOrderLocalTime: int = rtnorderlocaltime

    @property
    def InvestorID(self):
        return self._InvestorID

    @InvestorID.setter
    def InvestorID(self, value: str):
        self._InvestorID = value

    @property
    def BrokerID(self):
        return self._BrokerID

    @BrokerID.setter
    def BrokerID(self, value: str):
        self._BrokerID = value

    @property
    def ExchangeID(self):
        return self._ExchangeID

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        self._ExchangeID = value

    @property
    def ProductID(self):
        return self._ProductID

    @ProductID.setter
    def ProductID(self, value: str):
        self._ProductID = value

    @property
    def ProductType(self):
        return self._ProductType

    @ProductType.setter
    def ProductType(self, value: int):
        self._ProductType = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def OrderTime(self):
        return self._OrderTime

    @OrderTime.setter
    def OrderTime(self, value: str):
        self._OrderTime = value

    @property
    def CancelTime(self):
        return self._CancelTime

    @CancelTime.setter
    def CancelTime(self, value: str):
        self._CancelTime = value

    @property
    def TradingDay(self):
        return self._TradingDay

    @TradingDay.setter
    def TradingDay(self, value: str):
        self._TradingDay = value

    @property
    def InsertDate(self):
        return self._InsertDate

    @InsertDate.setter
    def InsertDate(self, value: str):
        self._InsertDate = value

    @property
    def UpdateTime(self):
        return self._UpdateTime

    @UpdateTime.setter
    def UpdateTime(self, value: str):
        self._UpdateTime = value

    @property
    def StatusMsg(self):
        return self._StatusMsg

    @StatusMsg.setter
    def StatusMsg(self, value: str):
        self._StatusMsg = value

    @property
    def FrontID(self):
        return self._FrontID

    @FrontID.setter
    def FrontID(self, value: int):
        self._FrontID = value

    @property
    def SessionID(self):
        return self._SessionID

    @SessionID.setter
    def SessionID(self, value: int):
        self._SessionID = value

    @property
    def OrderRef(self):
        return self._OrderRef

    @OrderRef.setter
    def OrderRef(self, value: str):
        self._OrderRef = value

    @property
    def OrderLocalNo(self):
        return self._OrderLocalNo

    @OrderLocalNo.setter
    def OrderLocalNo(self, value: str):
        self._OrderLocalNo = value

    @property
    def OrderID(self):
        return self._OrderID

    @OrderID.setter
    def OrderID(self, value: str):
        self._OrderID = value

    @property
    def RelativeOrderSysID(self):
        return self._RelativeOrderSysID

    @RelativeOrderSysID.setter
    def RelativeOrderSysID(self, value: str):
        self._RelativeOrderSysID = value

    @property
    def BrokerOrderSeq(self):
        return self._BrokerOrderSeq

    @BrokerOrderSeq.setter
    def BrokerOrderSeq(self, value: str):
        self._BrokerOrderSeq = value

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, value: float):
        self._Price = value

    @property
    def StopPrice(self):
        return self._StopPrice

    @StopPrice.setter
    def StopPrice(self, value: float):
        self._StopPrice = value

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, value: int):
        self._Volume = value

    @property
    def NoTradedVolume(self):
        return self._NoTradedVolume

    @NoTradedVolume.setter
    def NoTradedVolume(self, value: int):
        self._NoTradedVolume = value

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, value: int):
        self._Status = value

    @property
    def Direction(self):
        return self._Direction

    @Direction.setter
    def Direction(self, value: int):
        self._Direction = value

    @property
    def OpenCloseType(self):
        return self._OpenCloseType

    @OpenCloseType.setter
    def OpenCloseType(self, value: int):
        self._OpenCloseType = value

    @property
    def PriceCond(self):
        return self._PriceCond

    @PriceCond.setter
    def PriceCond(self, value: int):
        self._PriceCond = value

    @property
    def TimeCond(self):
        return self._TimeCond

    @TimeCond.setter
    def TimeCond(self, value: int):
        self._TimeCond = value

    @property
    def VolumeCond(self):
        return self._VolumeCond

    @VolumeCond.setter
    def VolumeCond(self, value: int):
        self._VolumeCond = value

    @property
    def HedgeType(self):
        return self._HedgeType

    @HedgeType.setter
    def HedgeType(self, value: int):
        self._HedgeType = value

    @property
    def OrderType(self):
        return self._OrderType

    @OrderType.setter
    def OrderType(self, value: int):
        self._OrderType = value

    @property
    def ActionType(self):
        return self._ActionType

    @ActionType.setter
    def ActionType(self, value: int):
        self._ActionType = value

    @property
    def ContingentCond(self):
        return self._ContingentCond

    @ContingentCond.setter
    def ContingentCond(self, value: int):
        self._ContingentCond = value

    @property
    def FrozenMarginPrice(self):
        return self._FrozenMarginPrice

    @FrozenMarginPrice.setter
    def FrozenMarginPrice(self, value: float):
        self._FrozenMarginPrice = value

    @property
    def FrozenMargin(self):
        return self._FrozenMargin

    @FrozenMargin.setter
    def FrozenMargin(self, value: float):
        self._FrozenMargin = value

    @property
    def FrozenCommission(self):
        return self._FrozenCommission

    @FrozenCommission.setter
    def FrozenCommission(self, value: float):
        self._FrozenCommission = value

    @property
    def ShowVolume(self):
        return self._ShowVolume

    @ShowVolume.setter
    def ShowVolume(self, value: int):
        self._ShowVolume = value

    @property
    def MinVolume(self):
        return self._MinVolume

    @MinVolume.setter
    def MinVolume(self, value: int):
        self._MinVolume = value

    @property
    def PricePrecision(self):
        return self._PricePrecision

    @PricePrecision.setter
    def PricePrecision(self, value: int):
        self._PricePrecision = value

    @property
    def FinBizNo(self):
        return self._FinBizNo

    @FinBizNo.setter
    def FinBizNo(self, value: str):
        self._FinBizNo = value

    @property
    def FinAlgoNo(self):
        return self._FinAlgoNo

    @FinAlgoNo.setter
    def FinAlgoNo(self, value: str):
        self._FinAlgoNo = value

    @property
    def FinInsertLocalTime(self):
        return self._FinInsertLocalTime

    @FinInsertLocalTime.setter
    def FinInsertLocalTime(self, value: int):
        self._FinInsertLocalTime = value

    @property
    def FinRtnOrderLocalTime(self):
        return self._FinRtnOrderLocalTime

    @FinRtnOrderLocalTime.setter
    def FinRtnOrderLocalTime(self, value: int):
        self._FinRtnOrderLocalTime = value

    @property
    def FinLockNo(self):
        return self._FinLockNo

    @FinLockNo.setter
    def FinLockNo(self, value: str):
        self._FinLockNo = value

    @property
    def BizName(self):
        return self._BizName

    @BizName.setter
    def BizName(self, value: str):
        self._BizName = value

    @property
    def RtnOrderLocalTime(self):
        return self._RtnOrderLocalTime

    @RtnOrderLocalTime.setter
    def RtnOrderLocalTime(self, value: int):
        self._RtnOrderLocalTime = value
