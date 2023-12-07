from typing import List
from ...interface import IData
from ...data.trade.TradeOrderData import TradeOrderData
from ...packer.trade.GetTradeOrdersParamDataPacker import GetTradeOrdersParamDataPacker


class GetTradeOrdersParamData(IData):
    def __init__(self, tradename: str = ''):
        super().__init__(GetTradeOrdersParamDataPacker(self))
        self._TradeName = tradename
        self._DataList: List[TradeOrderData] = []

    @property
    def TradeName(self):
        return self._TradeName

    @TradeName.setter
    def TradeName(self, value: str):
        self._TradeName = value

    @property
    def DataList(self):
        return self._DataList

    @DataList.setter
    def DataList(self, value: List[TradeOrderData]):
        self._DataList: List[TradeOrderData] = value
