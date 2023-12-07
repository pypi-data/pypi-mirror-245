from ...interface import IData
from ...packer.trade.TradeParamDataPacker import TradeParamDataPacker


class TradeParamData(IData):
    def __init__(self, tradenames: str = ''):
        super().__init__(TradeParamDataPacker(self))
        self._TradeNames = tradenames

    @property
    def TradeNames(self):
        return self._TradeNames

    @TradeNames.setter
    def TradeNames(self, value: str):
        self._TradeNames = value
