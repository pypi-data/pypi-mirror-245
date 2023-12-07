from typing import List
from ...interface import IData
from ...packer.market.SaveOHLCListParamDataPacker import SaveOHLCListParamDataPacker


class SaveOHLCListParamData(IData):
    def __init__(self, marketname: str = '', exchangeid: str = '', instrumentid: str = '',
                 range: int = 60, tradingday: str = '', actionday: str = '', presettlementprice: float = 0.0,
                 actiontimespanlist: List[int] = [],
                 tradingtimelist: List[str] = [],
                 starttimelist: List[str] = [],
                 endtimelist: List[str] = [],
                 totalturnoverlist: List[float] = [],
                 openinterestlist: List[float] = [],
                 openpricelist: List[float] = [],
                 openbidpricelist: List[float] = [],
                 openaskpricelist: List[float] = [],
                 openbidvolumelist: List[int] = [],
                 openaskvolumelist: List[int] = [],
                 highpricelist: List[float] = [],
                 highbidpricelist: List[float] = [],
                 highaskpricelist: List[float] = [],
                 highbidvolumelist: List[int] = [],
                 highaskvolumelist: List[int] = [],
                 lowerpricelist: List[float] = [],
                 lowerbidpricelist: List[float] = [],
                 loweraskpricelist: List[float] = [],
                 lowerbidvolumelist: List[int] = [],
                 loweraskvolumelist: List[int] = [],
                 closepricelist: List[float] = [],
                 closebidpricelist: List[float] = [],
                 closeaskpricelist: List[float] = [],
                 closebidvolumelist: List[int] = [],
                 closeaskvolumelist: List[int] = []
                 ):
        super().__init__(SaveOHLCListParamDataPacker(self))
        self._MarketName: str = marketname
        self._ExchangeID: str = exchangeid
        self._InstrumentID: str = instrumentid
        self._Range: int = range
        self._TradingDay: str = tradingday
        self._ActionDay: str = actionday
        self._PreSettlementPrice: float = presettlementprice
        self._ActionTimespanList: List[int] = actiontimespanlist
        self._TradingTimeList: List[str] = tradingtimelist
        self._StartTimeList: List[str] = starttimelist
        self._EndTimeList: List[str] = endtimelist
        self._TotalTurnoverList: List[float] = totalturnoverlist
        self._OpenInterestList: List[float] = openinterestlist
        self._OpenPriceList: List[float] = openpricelist
        self._OpenBidPriceList: List[float] = openbidpricelist
        self._OpenAskPriceList: List[float] = openaskpricelist
        self._OpenBidVolumeList: List[int] = openbidvolumelist
        self._OpenAskVolumeList: List[int] = openaskvolumelist

        self._HighPriceList: List[float] = highpricelist
        self._HighBidPriceList: List[float] = highbidpricelist
        self._HighAskPriceList: List[float] = highaskpricelist
        self._HighBidVolumeList: List[int] = highbidvolumelist
        self._HighAskVolumeList: List[int] = highaskvolumelist

        self._LowerPriceList: List[float] = lowerpricelist
        self._LowerBidPriceList: List[float] = lowerbidpricelist
        self._LowerAskPriceList: List[float] = loweraskpricelist
        self._LowerBidVolumeList: List[int] = lowerbidvolumelist
        self._LowerAskVolumeList: List[int] = loweraskvolumelist

        self._ClosePriceList: List[float] = closepricelist
        self._CloseBidPriceList: List[float] = closebidpricelist
        self._CloseAskPriceList: List[float] = closeaskpricelist
        self._CloseBidVolumeList: List[int] = closebidvolumelist
        self._CloseAskVolumeList: List[int] = closeaskvolumelist

    @property
    def MarketName(self):
        return self._MarketName

    @MarketName.setter
    def MarketName(self, value: str):
        self._MarketName = value

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
    def Range(self):
        return self._Range

    @Range.setter
    def Range(self, value: int):
        self._Range = value

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
    def PreSettlementPrice(self):
        return self._PreSettlementPrice

    @PreSettlementPrice.setter
    def PreSettlementPrice(self, value: float):
        self._PreSettlementPrice = value

    @property
    def ActionTimespanList(self):
        return self._ActionTimespanList

    @ActionTimespanList.setter
    def ActionTimespanList(self, value: List[int]):
        self._ActionTimespanList = value

    @property
    def TradingTimeList(self):
        return self._TradingTimeList

    @TradingTimeList.setter
    def TradingTimeList(self, value: List[str]):
        self._TradingTimeList = value

    @property
    def StartTimeList(self):
        return self._StartTimeList

    @StartTimeList.setter
    def StartTimeList(self, value: List[str]):
        self._StartTimeList = value

    @property
    def EndTimeList(self):
        return self._EndTimeList

    @EndTimeList.setter
    def EndTimeList(self, value: List[str]):
        self._EndTimeList = value

    @property
    def TotalTurnoverList(self):
        return self._TotalTurnoverList

    @TotalTurnoverList.setter
    def TotalTurnoverList(self, value: List[float]):
        self._TotalTurnoverList = value

    @property
    def OpenInterestList(self):
        return self._OpenInterestList

    @OpenInterestList.setter
    def OpenInterestList(self, value: List[float]):
        self._OpenInterestList = value

    @property
    def OpenPriceList(self):
        return self._OpenPriceList

    @OpenPriceList.setter
    def OpenPriceList(self, value: List[float]):
        self._OpenPriceList = value

    @property
    def OpenBidPriceList(self):
        return self._OpenBidPriceList

    @OpenBidPriceList.setter
    def OpenBidPriceList(self, value: List[float]):
        self._OpenBidPriceList = value

    @property
    def OpenAskPriceList(self):
        return self._OpenAskPriceList

    @OpenAskPriceList.setter
    def OpenAskPriceList(self, value: List[float]):
        self._OpenAskPriceList = value

    @property
    def OpenBidVolumeList(self):
        return self._OpenBidVolumeList

    @OpenBidVolumeList.setter
    def OpenBidVolumeList(self, value: List[int]):
        self._OpenBidVolumeList = value

    @property
    def OpenAskVolumeList(self):
        return self._OpenAskVolumeList

    @OpenAskVolumeList.setter
    def OpenAskVolumeList(self, value: List[int]):
        self._OpenAskVolumeList = value

    @property
    def HighPriceList(self):
        return self._HighPriceList

    @HighPriceList.setter
    def HighPriceList(self, value: List[float]):
        self._HighPriceList = value

    @property
    def HighBidPriceList(self):
        return self._HighBidPriceList

    @HighBidPriceList.setter
    def HighBidPriceList(self, value: List[float]):
        self._HighBidPriceList = value

    @property
    def HighAskPriceList(self):
        return self._HighAskPriceList

    @HighAskPriceList.setter
    def HighAskPriceList(self, value: List[float]):
        self._HighAskPriceList = value

    @property
    def HighBidVolumeList(self):
        return self._HighBidVolumeList

    @HighBidVolumeList.setter
    def HighBidVolumeList(self, value: List[int]):
        self._HighBidVolumeList = value

    @property
    def HighAskVolumeList(self):
        return self._HighAskVolumeList

    @HighAskVolumeList.setter
    def HighAskVolumeList(self, value: List[int]):
        self._HighAskVolumeList = value

    @property
    def LowerPriceList(self):
        return self._LowerPriceList

    @LowerPriceList.setter
    def LowerPriceList(self, value: List[float]):
        self._LowerPriceList = value

    @property
    def LowerBidPriceList(self):
        return self._LowerBidPriceList

    @LowerBidPriceList.setter
    def LowerBidPriceList(self, value: List[float]):
        self._LowerBidPriceList = value

    @property
    def LowerAskPriceList(self):
        return self._LowerAskPriceList

    @LowerAskPriceList.setter
    def LowerAskPriceList(self, value: List[float]):
        self._LowerAskPriceList = value

    @property
    def LowerBidVolumeList(self):
        return self._LowerBidVolumeList

    @LowerBidVolumeList.setter
    def LowerBidVolumeList(self, value: List[int]):
        self._LowerBidVolumeList = value

    @property
    def LowerAskVolumeList(self):
        return self._LowerAskVolumeList

    @LowerAskVolumeList.setter
    def LowerAskVolumeList(self, value: List[int]):
        self._LowerAskVolumeList = value

    @property
    def ClosePriceList(self):
        return self._ClosePriceList

    @ClosePriceList.setter
    def ClosePriceList(self, value: List[float]):
        self._ClosePriceList = value

    @property
    def CloseBidPriceList(self):
        return self._CloseBidPriceList

    @CloseBidPriceList.setter
    def CloseBidPriceList(self, value: List[float]):
        self._CloseBidPriceList = value

    @property
    def CloseAskPriceList(self):
        return self._CloseAskPriceList

    @CloseAskPriceList.setter
    def CloseAskPriceList(self, value: List[float]):
        self._CloseAskPriceList = value

    @property
    def CloseBidVolumeList(self):
        return self._CloseBidVolumeList

    @CloseBidVolumeList.setter
    def CloseBidVolumeList(self, value: List[int]):
        self._CloseBidVolumeList = value

    @property
    def CloseAskVolumeList(self):
        return self._CloseAskVolumeList

    @CloseAskVolumeList.setter
    def CloseAskVolumeList(self, value: List[int]):
        self._CloseAskVolumeList = value
