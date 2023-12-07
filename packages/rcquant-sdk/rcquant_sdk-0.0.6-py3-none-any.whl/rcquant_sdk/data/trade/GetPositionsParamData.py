from typing import List
from ...interface import IData
from ...data.trade.PositionData import PositionData
from ...packer.trade.GetPositionsParamDataPacker import GetPositionsParamDataPacker


class GetPositionsParamData(IData):
    def __init__(self, tradename: str = '', exchangeid: str = '', instrumentid: str = ''):
        super().__init__(GetPositionsParamDataPacker(self))
        self._TradeName = tradename
        self._ExchangeID = exchangeid
        self._InstrumentID = instrumentid
        self._DataList: List[PositionData] = []

    @property
    def TradeName(self):
        return self._TradeName

    @TradeName.setter
    def TradeName(self, value: str):
        self._TradeName = value

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
    def DataList(self):
        return self._DataList

    @DataList.setter
    def DataList(self, value: List[PositionData]):
        self._DataList: List[PositionData] = value
