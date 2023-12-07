from ...interface import IData
from ...packer.market.SubOHLCParamDataPacker import SubOHLCParamDataPacker


class SubOHLCParamData(IData):
    def __init__(self, marketname: str = '', exchangeid: str = '', instrumentid: str = '', range: str = "60"):
        super().__init__(SubOHLCParamDataPacker(self))
        self._MarketName: str = marketname
        self._ExchangeID: str = exchangeid
        self._InstrumentID: str = instrumentid
        self._Range: str = range

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
