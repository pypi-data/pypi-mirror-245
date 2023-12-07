from ...interface import IData
from ...packer.chart.ValueAxisParamDataPacker import ValueAxisParamDataPacker


class ValueAxisParamData(IData):
    def __init__(self, plotindex: int = -1, valueaxisid: int = -1, maxticknum: int = 6, steps: float = -1.0, format: str = '',
                 labeltextlen: int = 6, validmul: float = -1.0, pricetick: float = 1.0, precision: int = 2):
        super().__init__(ValueAxisParamDataPacker(self))
        self._PlotIndex: int = plotindex
        self._ValueAxisID: int = valueaxisid
        self._MaxTickNum: int = maxticknum
        self._Steps: float = steps
        self._Format: str = format
        self._LabelTextLen: int = labeltextlen
        self._ValidMul: float = validmul
        self._PriceTick: float = pricetick
        self._Precision: int = precision

    @property
    def PlotIndex(self):
        return self._PlotIndex

    @PlotIndex.setter
    def PlotIndex(self, value: int):
        self._PlotIndex = value

    @property
    def ValueAxisID(self):
        return self._ValueAxisID

    @ValueAxisID.setter
    def ValueAxisID(self, value: int):
        self._ValueAxisID = value

    @property
    def MaxTickNum(self):
        return self._MaxTickNum

    @MaxTickNum.setter
    def MaxTickNum(self, value: int):
        self._MaxTickNum = value

    @property
    def Steps(self):
        return self._Steps

    @Steps.setter
    def Steps(self, value: float):
        self._Steps = value

    @property
    def Format(self):
        return self._Format

    @Format.setter
    def Format(self, value: str):
        self._Format = value

    @property
    def LabelTextLen(self):
        return self._LabelTextLen

    @LabelTextLen.setter
    def LabelTextLen(self, value: int):
        self._LabelTextLen = value

    @property
    def ValidMul(self):
        return self._ValidMul

    @ValidMul.setter
    def ValidMul(self, value: float):
        self._ValidMul = value

    @property
    def PriceTick(self):
        return self._PriceTick

    @PriceTick.setter
    def PriceTick(self, value: float):
        self._PriceTick = value

    @property
    def Precision(self):
        return self._Precision

    @Precision.setter
    def Precision(self, value: int):
        self._Precision = value
