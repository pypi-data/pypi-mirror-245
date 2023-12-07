from typing import Dict
from ...interface import IData
from ...packer.chart.BarGraphParamDataPacker import BarGraphParamDataPacker


class BarGraphParamData(IData):
    def __init__(self, id: str = '', name: str = '', style: int = 0, framestyle: int = 0, color: str = "white", pricetick: float = 1.0,
                 tickvalidmul: float = -1.0, linewidth: int = 1, plotindex: int = 0,
                 valueaxisid: int = -1, showlegend: bool = True, legendformat: str = '', legendcolor: str = "", joinvalueaxis: bool = True,
                 validmaxvalue: float = 9999999.99, validminvalue: float = -9999999.99, userdata: Dict[str, str] = {}):
        super().__init__(BarGraphParamDataPacker(self))
        self._ID: str = id
        self._Name: str = name
        self._Style: int = style
        self._FrameStyle: int = framestyle
        self._Color: str = color
        self._PriceTick: float = pricetick
        self._LineWidth: int = linewidth
        self._PlotIndex: int = plotindex
        self._ValueAxisID: int = valueaxisid
        self._ShowLegend: bool = showlegend
        self._LegendFormat: str = legendformat
        self._LegendColor: str = legendcolor
        self._JoinValueAxis: bool = joinvalueaxis
        self._TickValidMul: float = tickvalidmul
        self._ValidMaxValue: float = validmaxvalue
        self._ValidMinValue: float = validminvalue
        self._UserData: Dict[str, str] = userdata

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value: str):
        self._ID = value

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, value: str):
        self._Name = value

    @property
    def Style(self):
        return self._Style

    @Style.setter
    def Style(self, value: int):
        self._Style = value

    @property
    def FrameStyle(self):
        return self._FrameStyle

    @FrameStyle.setter
    def FrameStyle(self, value: int):
        self._FrameStyle = value

    @property
    def Color(self):
        return self._Color

    @Color.setter
    def Color(self, value: str):
        self._Color = value

    @property
    def PriceTick(self):
        return self._PriceTick

    @PriceTick.setter
    def PriceTick(self, value):
        self._PriceTick = float(value)

    @property
    def LineWidth(self):
        return self._LineWidth

    @LineWidth.setter
    def LineWidth(self, value: int):
        self._LineWidth = value

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
    def ShowLegend(self):
        return self._ShowLegend

    @ShowLegend.setter
    def ShowLegend(self, value: bool):
        self._ShowLegend = value

    @property
    def LegendFormat(self):
        return self._LegendFormat

    @LegendFormat.setter
    def LegendFormat(self, value: str):
        self._LegendFormat = value

    @property
    def LegendColor(self):
        return self._LegendColor

    @LegendColor.setter
    def LegendColor(self, value: str):
        self._LegendColor = value

    @property
    def JoinValueAxis(self):
        return self._JoinValueAxis

    @JoinValueAxis.setter
    def JoinValueAxis(self, value: bool):
        self._JoinValueAxis = value

    @property
    def ValidMaxValue(self):
        return self._ValidMaxValue

    @ValidMaxValue.setter
    def ValidMaxValue(self, value):
        self._ValidMaxValue = float(value)

    @property
    def ValidMinValue(self):
        return self._ValidMinValue

    @ValidMinValue.setter
    def ValidMinValue(self, value):
        self._ValidMinValue = float(value)

    @property
    def TickValidMul(self):
        return self._TickValidMul

    @TickValidMul.setter
    def TickValidMul(self, value):
        self._TickValidMul = float(value)

    @property
    def UserData(self):
        return self._UserData

    @UserData.setter
    def UserData(self, value: Dict[str, str]):
        self._UserData = value
