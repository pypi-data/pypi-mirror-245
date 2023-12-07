from ...interface import IData
from ...packer.chart.LegendItemParamDataPacker import LegendItemParamDataPacker


class LegendItemParamData(IData):
    def __init__(self, plotindex: int = 0, type: int = 0, halgin: int = 1, valgin: int = 1, itemmargin: int = 2, itemspace: int = 2, hoffset: int = 2, voffset: int = 2,
                 maxcolumns: int = 8, borderwidth: int = 1, bordercolor: str = "", borderradius: int = 4, backgroundalpha: int = 240, backgroundcolor: str = ''):
        super().__init__(LegendItemParamDataPacker(self))
        self._PlotIndex: int = plotindex
        self._Type: int = type
        self._HAlgin: int = halgin
        self._VAlgin: int = valgin
        self._ItemMargin: int = itemmargin
        self._ItemSpace: int = itemspace
        self._HOffset: int = hoffset
        self._VOffset: int = voffset
        self._MaxColumns: int = maxcolumns
        self._BorderWidth: int = borderwidth
        self._BorderColor: str = bordercolor
        self._BorderRadius: int = borderradius
        self._BackGroundAlpha: int = backgroundalpha
        self._BackGroundColor: str = backgroundcolor

    @property
    def PlotIndex(self):
        return self._PlotIndex

    @PlotIndex.setter
    def PlotIndex(self, value: int):
        self._PlotIndex = value

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, value: int):
        self._Type = value

    @property
    def HAlgin(self):
        return self._HAlgin

    @HAlgin.setter
    def HAlgin(self, value: int):
        self._HAlgin = value

    @property
    def VAlgin(self):
        return self._VAlgin

    @VAlgin.setter
    def VAlgin(self, value: int):
        self._VAlgin = value

    @property
    def ItemMargin(self):
        return self._ItemMargin

    @ItemMargin.setter
    def ItemMargin(self, value: int):
        self._ItemMargin = value

    @property
    def ItemSpace(self):
        return self._ItemSpace

    @ItemSpace.setter
    def ItemSpace(self, value: int):
        self._ItemSpace = value

    @property
    def HOffset(self):
        return self._HOffset

    @HOffset.setter
    def HOffset(self, value: int):
        self._HOffset = value

    @property
    def VOffset(self):
        return self._VOffset

    @VOffset.setter
    def VOffset(self, value: int):
        self._VOffset = value

    @property
    def MaxColumns(self):
        return self._MaxColumns

    @MaxColumns.setter
    def MaxColumns(self, value: int):
        self._MaxColumns = value

    @property
    def BorderWidth(self):
        return self._BorderWidth

    @BorderWidth.setter
    def BorderWidth(self, value: int):
        self._BorderWidth = value

    @property
    def BorderColor(self):
        return self._BorderColor

    @BorderColor.setter
    def BorderColor(self, value: str):
        self._BorderColor = value

    @property
    def BorderRadius(self):
        return self._BorderRadius

    @BorderRadius.setter
    def BorderRadius(self, value: int):
        self._BorderRadius = value

    @property
    def BackGroundAlpha(self):
        return self._BackGroundAlpha

    @BackGroundAlpha.setter
    def BackGroundAlpha(self, value: int):
        self._BackGroundAlpha = value

    @property
    def BackGroundColor(self):
        return self._BackGroundColor

    @BackGroundColor.setter
    def BackGroundColor(self, value: str):
        self._BackGroundColor = value
