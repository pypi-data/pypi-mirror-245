from ...interface import IData
from ...data.market.OHLCData import OHLCData
from ...packer.chart.OHLCValueDataPacker import OHLCValueDataPacker


class OHLCValueData(IData):
    def __init__(self, graphid: str = '', ohlcdata: OHLCData = None):
        super().__init__(OHLCValueDataPacker(self))
        self._GraphID: str = graphid
        self._OHLC: OHLCData = ohlcdata

    @property
    def GraphID(self):
        return self._GraphID

    @GraphID.setter
    def GraphID(self, value: str):
        self._GraphID = value

    @property
    def OHLC(self):
        return self._OHLC

    @OHLC.setter
    def OHLC(self, value: OHLCData):
        self._OHLC = value
