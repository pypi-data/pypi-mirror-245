from ...interface import IData
from ...packer.chart.PlotParamDataPacker import PlotParamDataPacker


class PlotParamData(IData):
    def __init__(self, plotindex: int = 0, plotname: str = '', plotnamecolor: str = 'white', height: int = 100, iseqvalueaxis: bool = True,
                 gridstyle: int = 2, gridcolor: str = "#323232", backgroundcolor: str = "black", bordercolor: str = "red", borderwidth: int = 1,
                 showlegenditem: bool = True, gridxstyle: int = 2, gridxcolor: str = '#323232'):
        super().__init__(PlotParamDataPacker(self))
        self._PlotIndex: int = plotindex
        self._Height: int = height
        self._IsEqValueAxis: bool = iseqvalueaxis
        self._GridStyle: int = gridstyle
        self._GridColor: str = gridcolor
        self._BackGroundColor: str = backgroundcolor
        self._BorderColor: str = bordercolor
        self._BorderWidth: int = borderwidth
        self._ShowLegendItem: bool = showlegenditem
        self._PlotName: str = plotname
        self._PlotNameColor: str = plotnamecolor
        self._GridXColor: str = gridxcolor
        self._GridXStyle: int = gridxstyle

    @property
    def PlotIndex(self):
        return self._PlotIndex

    @PlotIndex.setter
    def PlotIndex(self, value: int):
        self._PlotIndex = value

    @property
    def PlotName(self):
        return self._PlotName

    @PlotName.setter
    def PlotName(self, value: int):
        self._PlotName = value

    @property
    def PlotNameColor(self):
        return self._PlotNameColor

    @PlotNameColor.setter
    def PlotNameColor(self, value: int):
        self._PlotNameColor = value

    @property
    def Height(self):
        return self._Height

    @Height.setter
    def Height(self, value: int):
        self._Height = value

    @property
    def IsEqValueAxis(self):
        return self._IsEqValueAxis

    @IsEqValueAxis.setter
    def IsEqValueAxis(self, value: bool):
        self._IsEqValueAxis = value

    @property
    def GridStyle(self):
        return self._GridStyle

    @GridStyle.setter
    def GridStyle(self, value: int):
        self._GridStyle = value

    @property
    def GridColor(self):
        return self._GridColor

    @GridColor.setter
    def GridColor(self, value: str):
        self._GridColor = value

    @property
    def BackGroundColor(self):
        return self._BackGroundColor

    @BackGroundColor.setter
    def BackGroundColor(self, value: str):
        self._BackGroundColor = value

    @property
    def BorderColor(self):
        return self._BorderColor

    @BorderColor.setter
    def BorderColor(self, value: str):
        self._BorderColor = value

    @property
    def BorderWidth(self):
        return self._BorderWidth

    @BorderWidth.setter
    def BorderWidth(self, value: int):
        self._BorderWidth = value

    @property
    def ShowLegendItem(self):
        return self._ShowLegendItem

    @ShowLegendItem.setter
    def ShowLegendItem(self, value: bool):
        self._ShowLegendItem = value

    @property
    def GridXStyle(self):
        return self._GridXStyle

    @GridXStyle.setter
    def GridXStyle(self, value: int):
        self._GridXStyle = value

    @property
    def GridXColor(self):
        return self._GridXColor

    @GridXColor.setter
    def GridXColor(self, value: str):
        self._GridXColor = value
