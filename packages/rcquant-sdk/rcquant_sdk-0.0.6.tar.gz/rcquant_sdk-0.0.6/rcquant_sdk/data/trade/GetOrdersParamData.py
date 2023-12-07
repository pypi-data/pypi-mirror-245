from typing import List
from ...interface import IData
from ...data.trade.OrderData import OrderData
from ...packer.trade.GetOrdersParamDataPacker import GetOrdersParamDataPacker


class GetOrdersParamData(IData):
    def __init__(self, tradename: str = ''):
        super().__init__(GetOrdersParamDataPacker(self))
        self._TradeName = tradename
        self._DataList: List[OrderData] = []

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
    def DataList(self, value: List[OrderData]):
        self._DataList: List[OrderData] = value
