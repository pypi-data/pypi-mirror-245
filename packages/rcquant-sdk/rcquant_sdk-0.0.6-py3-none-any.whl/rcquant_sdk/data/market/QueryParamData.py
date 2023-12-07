from ...interface import IData
from ...packer.market.QueryParamDataPacker import QueryParamDataPacker


class QueryParamData(IData):
    def __init__(self, marketname: str = '', investorid: str = '', brokerid: str = '', exchangeid: str = '', exchangeinstid: str = '', instrumentid: str = '', producttype: int = 0,
                 productid: str = '', orderid: str = '', tradeid: str = '', inserttimestart: str = '', inserttimeend: str = '', tradetimestart: str = '', tradetimeend: str = '',
                 currencyid: str = '', hedgetype: int = 0):
        super().__init__(QueryParamDataPacker(self))
        self._MarketName: str = marketname
        self._InvestorID: str = investorid
        self._BrokerID: str = brokerid
        self._ExchangeID: str = exchangeid
        self._ExchangeInstID: str = exchangeinstid
        self._InstrumentID: str = instrumentid
        self._ProductType: int = producttype
        self._ProductID: str = productid
        self._OrderID: str = orderid
        self._TradeID: str = tradeid
        self._InsertTimeStart: str = inserttimestart
        self._InsertTimeEnd: str = inserttimeend
        self._TradeTimeStart: str = tradetimestart
        self._TradeTimeEnd: str = tradetimeend
        self._CurrencyID: str = currencyid
        self._HedgeType: int = hedgetype

    @property
    def MarketName(self):
        return self._MarketName

    @MarketName.setter
    def MarketName(self, value: str):
        self._MarketName = value

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
    def ExchangeInstID(self):
        return self._ExchangeInstID

    @ExchangeInstID.setter
    def ExchangeInstID(self, value: str):
        self._ExchangeInstID = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def ProductType(self):
        return self._ProductType

    @ProductType.setter
    def ProductType(self, value: int):
        self._ProductType = value

    @property
    def ProductID(self):
        return self._ProductID

    @ProductID.setter
    def ProductID(self, value: str):
        self._ProductID = value

    @property
    def OrderID(self):
        return self._OrderID

    @OrderID.setter
    def OrderID(self, value: str):
        self._OrderID = value

    @property
    def TradeID(self):
        return self._TradeID

    @TradeID.setter
    def TradeID(self, value: str):
        self._TradeID = value

    @property
    def InsertTimeStart(self):
        return self._InsertTimeStart

    @InsertTimeStart.setter
    def InsertTimeStart(self, value: str):
        self._InsertTimeStart = value

    @property
    def InsertTimeEnd(self):
        return self._InsertTimeEnd

    @InsertTimeEnd.setter
    def InsertTimeEnd(self, value: str):
        self._InsertTimeEnd = value

    @property
    def TradeTimeStart(self):
        return self._TradeTimeStart

    @TradeTimeStart.setter
    def TradeTimeStart(self, value: str):
        self._TradeTimeStart = value

    @property
    def TradeTimeEnd(self):
        return self._TradeTimeEnd

    @TradeTimeEnd.setter
    def TradeTimeEnd(self, value: str):
        self._TradeTimeEnd = value

    @property
    def CurrencyID(self):
        return self._CurrencyID

    @CurrencyID.setter
    def CurrencyID(self, value: str):
        self._CurrencyID = value

    @property
    def HedgeType(self):
        return self._HedgeType

    @HedgeType.setter
    def HedgeType(self, value: int):
        self._HedgeType = value
