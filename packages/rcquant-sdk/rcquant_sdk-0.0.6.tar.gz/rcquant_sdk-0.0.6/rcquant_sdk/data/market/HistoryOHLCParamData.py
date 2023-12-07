from typing import List
from ...interface import IData
from ...data.market.OHLCData import OHLCData
from ...packer.market.HistoryOHLCParamDataPacker import HistoryOHLCParamDataPacker


class HistoryOHLCParamData(IData):
    def __init__(self, marketname: str = '', exchangeid: str = '', instrumentid: str = '', range: str = "60", startdate: str = '', enddate: str = '', ohlclist: list = '', isreturnlist: bool = False):
        super().__init__(HistoryOHLCParamDataPacker(self))
        self._MarketName: str = marketname
        self._ExchangeID: str = exchangeid
        self._InstrumentID: str = instrumentid
        self._Range: str = range
        self._StartDate: str = startdate
        self._EndDate: str = enddate
        self._OHLCList: list = ohlclist
        self._IsReturnList: bool = isreturnlist

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
    def Range(self, value: str):
        self._Range = value

    @property
    def StartDate(self):
        return self._StartDate

    @StartDate.setter
    def StartDate(self, value: str):
        self._StartDate = value

    @property
    def EndDate(self):
        return self._EndDate

    @EndDate.setter
    def EndDate(self, value: str):
        self._EndDate = value

    @property
    def OHLCList(self):
        return self._OHLCList

    @OHLCList.setter
    def OHLCList(self, value: list):
        self._OHLCList = value

    @property
    def IsReturnList(self):
        return self._IsReturnList

    @IsReturnList.setter
    def IsReturnList(self, value: bool):
        self._IsReturnList = value
