from ...interface import IData
from ...packer.market.MarketParamDataPacker import MarketParamDataPacker


class MarketParamData(IData):
    def __init__(self, marketnames: str = ''):
        super().__init__(MarketParamDataPacker(self))
        self._MarketNames = marketnames

    @property
    def MarketNames(self):
        return self._MarketNames

    @MarketNames.setter
    def MarketNames(self, value: str):
        self._MarketNames = value
