from ...interface import IData
from ...packer.market.TickDataPacker import TickDataPacker


class TickData(IData):
    def __init__(self, instrumentid: str = '', exchangeid: str = '', tradingday: str = '', actionday: str = '', tradingtime: str = '',
                 lastprice: float = 0.0, lastvolume: int = 0, askprice: float = 0.0, askvolume: int = 0, bidprice: float = 0.0, bidvolume: int = 0):
        super().__init__(TickDataPacker(self))
        self._InstrumentID: str = instrumentid
        self._ExchangeID: str = exchangeid
        self._TradingDay: str = tradingday
        self._ActionDay: str = actionday
        self._TradingTime: str = tradingtime
        self._LastPrice: float = lastprice
        self._LastVolume: int = lastvolume
        self._AskPrice: float = askprice
        self._AskVolume: int = askvolume
        self._BidPrice: float = bidprice
        self._BidVolume: int = bidvolume

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def ExchangeID(self):
        return self._ExchangeID

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        self._ExchangeID = value

    @property
    def TradingDay(self):
        return self._TradingDay

    @TradingDay.setter
    def TradingDay(self, value: str):
        self._TradingDay = value

    @property
    def ActionDay(self):
        return self._ActionDay

    @ActionDay.setter
    def ActionDay(self, value: str):
        self._ActionDay = value

    @property
    def TradingTime(self):
        return self._TradingTime

    @TradingTime.setter
    def TradingTime(self, value: str):
        self._TradingTime = value

    @property
    def LastPrice(self):
        return self._LastPrice

    @LastPrice.setter
    def LastPrice(self, value: float):
        self._LastPrice = value

    @property
    def LastVolume(self):
        return self._LastVolume

    @LastVolume.setter
    def LastVolume(self, value: int):
        self._LastVolume = value

    @property
    def AskPrice(self):
        return self._AskPrice

    @AskPrice.setter
    def AskPrice(self, value: float):
        self._AskPrice = value

    @property
    def AskVolume(self):
        return self._AskVolume

    @AskVolume.setter
    def AskVolume(self, value: int):
        self._AskVolume = value

    @property
    def BidPrice(self):
        return self._BidPrice

    @BidPrice.setter
    def BidPrice(self, value: float):
        self._BidPrice = value

    @property
    def BidVolume(self):
        return self._BidVolume

    @BidVolume.setter
    def BidVolume(self, value: int):
        self._BidVolume = value
