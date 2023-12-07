from ...interface import IData
from ...packer.market.OHLCDataPacker import OHLCDataPacker


class OHLCData(IData):
    def __init__(self, exchangeid: str = '', instrumentid: str = '', tradingday: str = '', tradingtime: str = '', starttime: str = '', endtime: str = '', actionday: str = '', actiontimespan: int = -1,
                 range: int = 60, index: int = -1, openprice: float = 0.0, highestprice: float = 0.0, lowestprice: float = 0.0, closeprice: float = 0.0, totalturnover: float = 0.0,
                 totalvolume: int = 0, openinterest: float = 0.0, presettlementprice: float = 0.0, changerate: float = 0.0, changevalue: float = 0.0, openbidprice: float = 0.0,
                 openaskprice: float = 0.0, openbidvolume: int = 0, openaskvolume: int = 0, highestbidprice: float = 0.0, highestaskprice: float = 0.0, highestbidvolume: int = 0,
                 highestaskvolume: int = 0, lowestbidprice: float = 0.0, lowestaskprice: float = 0.0, lowestbidvolume: int = 0, lowestaskvolume: int = 0, closebidprice: float = 0.0,
                 closeaskprice: float = 0.0, closebidvolume: int = 0, closeaskvolume: int = 0):
        super().__init__(OHLCDataPacker(self))
        self._ExchangeID: str = exchangeid
        self._InstrumentID: str = instrumentid
        self._TradingDay: str = tradingday
        self._TradingTime: str = tradingtime
        self._StartTime: str = starttime
        self._EndTime: str = endtime
        self._ActionDay: str = actionday
        self._ActionTimeSpan: int = actiontimespan
        self._Range: int = range
        self._Index: int = index
        self._OpenPrice: float = openprice
        self._HighestPrice: float = highestprice
        self._LowestPrice: float = lowestprice
        self._ClosePrice: float = closeprice
        self._TotalTurnover: float = totalturnover
        self._TotalVolume: int = totalvolume
        self._OpenInterest: float = openinterest
        self._PreSettlementPrice: float = presettlementprice
        self._ChangeRate: float = changerate
        self._ChangeValue: float = changevalue
        self._OpenBidPrice: float = openbidprice
        self._OpenAskPrice: float = openaskprice
        self._OpenBidVolume: int = openbidvolume
        self._OpenAskVolume: int = openaskvolume
        self._HighestBidPrice: float = highestbidprice
        self._HighestAskPrice: float = highestaskprice
        self._HighestBidVolume: int = highestbidvolume
        self._HighestAskVolume: int = highestaskvolume
        self._LowestBidPrice: float = lowestbidprice
        self._LowestAskPrice: float = lowestaskprice
        self._LowestBidVolume: int = lowestbidvolume
        self._LowestAskVolume: int = lowestaskvolume
        self._CloseBidPrice: float = closebidprice
        self._CloseAskPrice: float = closeaskprice
        self._CloseBidVolume: int = closebidvolume
        self._CloseAskVolume: int = closeaskvolume

    @property
    def ExchangeID(self):
        return self._ExchangeID

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        self._ExchangeID = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def TradingDay(self):
        return self._TradingDay

    @TradingDay.setter
    def TradingDay(self, value: str):
        self._TradingDay = value

    @property
    def TradingTime(self):
        return self._TradingTime

    @TradingTime.setter
    def TradingTime(self, value: str):
        self._TradingTime = value

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, value: str):
        self._StartTime = value

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, value: str):
        self._EndTime = value

    @property
    def ActionDay(self):
        return self._ActionDay

    @ActionDay.setter
    def ActionDay(self, value: str):
        self._ActionDay = value

    @property
    def ActionTimeSpan(self):
        return self._ActionTimeSpan

    @ActionTimeSpan.setter
    def ActionTimeSpan(self, value: int):
        self._ActionTimeSpan = value

    @property
    def Range(self):
        return self._Range

    @Range.setter
    def Range(self, value: int):
        self._Range = value

    @property
    def Index(self):
        return self._Index

    @Index.setter
    def Index(self, value: int):
        self._Index = value

    @property
    def OpenPrice(self):
        return self._OpenPrice

    @OpenPrice.setter
    def OpenPrice(self, value: float):
        self._OpenPrice = value

    @property
    def HighestPrice(self):
        return self._HighestPrice

    @HighestPrice.setter
    def HighestPrice(self, value: float):
        self._HighestPrice = value

    @property
    def LowestPrice(self):
        return self._LowestPrice

    @LowestPrice.setter
    def LowestPrice(self, value: float):
        self._LowestPrice = value

    @property
    def ClosePrice(self):
        return self._ClosePrice

    @ClosePrice.setter
    def ClosePrice(self, value: float):
        self._ClosePrice = value

    @property
    def TotalTurnover(self):
        return self._TotalTurnover

    @TotalTurnover.setter
    def TotalTurnover(self, value: float):
        self._TotalTurnover = value

    @property
    def TotalVolume(self):
        return self._TotalVolume

    @TotalVolume.setter
    def TotalVolume(self, value: int):
        self._TotalVolume = value

    @property
    def OpenInterest(self):
        return self._OpenInterest

    @OpenInterest.setter
    def OpenInterest(self, value: float):
        self._OpenInterest = value

    @property
    def PreSettlementPrice(self):
        return self._PreSettlementPrice

    @PreSettlementPrice.setter
    def PreSettlementPrice(self, value: float):
        self._PreSettlementPrice = value

    @property
    def ChangeRate(self):
        return self._ChangeRate

    @ChangeRate.setter
    def ChangeRate(self, value: float):
        self._ChangeRate = value

    @property
    def ChangeValue(self):
        return self._ChangeValue

    @ChangeValue.setter
    def ChangeValue(self, value: float):
        self._ChangeValue = value

    @property
    def OpenBidPrice(self):
        return self._OpenBidPrice

    @OpenBidPrice.setter
    def OpenBidPrice(self, value: float):
        self._OpenBidPrice = value

    @property
    def OpenAskPrice(self):
        return self._OpenAskPrice

    @OpenAskPrice.setter
    def OpenAskPrice(self, value: float):
        self._OpenAskPrice = value

    @property
    def OpenBidVolume(self):
        return self._OpenBidVolume

    @OpenBidVolume.setter
    def OpenBidVolume(self, value: int):
        self._OpenBidVolume = value

    @property
    def OpenAskVolume(self):
        return self._OpenAskVolume

    @OpenAskVolume.setter
    def OpenAskVolume(self, value: int):
        self._OpenAskVolume = value

    @property
    def HighestBidPrice(self):
        return self._HighestBidPrice

    @HighestBidPrice.setter
    def HighestBidPrice(self, value: float):
        self._HighestBidPrice = value

    @property
    def HighestAskPrice(self):
        return self._HighestAskPrice

    @HighestAskPrice.setter
    def HighestAskPrice(self, value: float):
        self._HighestAskPrice = value

    @property
    def HighestBidVolume(self):
        return self._HighestBidVolume

    @HighestBidVolume.setter
    def HighestBidVolume(self, value: int):
        self._HighestBidVolume = value

    @property
    def HighestAskVolume(self):
        return self._HighestAskVolume

    @HighestAskVolume.setter
    def HighestAskVolume(self, value: int):
        self._HighestAskVolume = value

    @property
    def LowestBidPrice(self):
        return self._LowestBidPrice

    @LowestBidPrice.setter
    def LowestBidPrice(self, value: float):
        self._LowestBidPrice = value

    @property
    def LowestAskPrice(self):
        return self._LowestAskPrice

    @LowestAskPrice.setter
    def LowestAskPrice(self, value: float):
        self._LowestAskPrice = value

    @property
    def LowestBidVolume(self):
        return self._LowestBidVolume

    @LowestBidVolume.setter
    def LowestBidVolume(self, value: int):
        self._LowestBidVolume = value

    @property
    def LowestAskVolume(self):
        return self._LowestAskVolume

    @LowestAskVolume.setter
    def LowestAskVolume(self, value: int):
        self._LowestAskVolume = value

    @property
    def CloseBidPrice(self):
        return self._CloseBidPrice

    @CloseBidPrice.setter
    def CloseBidPrice(self, value: float):
        self._CloseBidPrice = value

    @property
    def CloseAskPrice(self):
        return self._CloseAskPrice

    @CloseAskPrice.setter
    def CloseAskPrice(self, value: float):
        self._CloseAskPrice = value

    @property
    def CloseBidVolume(self):
        return self._CloseBidVolume

    @CloseBidVolume.setter
    def CloseBidVolume(self, value: int):
        self._CloseBidVolume = value

    @property
    def CloseAskVolume(self):
        return self._CloseAskVolume

    @CloseAskVolume.setter
    def CloseAskVolume(self, value: int):
        self._CloseAskVolume = value
