from typing import Dict
from ...interface import IData
from ...packer.chart.LineGraphParamDataPacker import LineGraphParamDataPacker


class LineGraphParamData(IData):
    def __init__(self, id: str = '', name: str = '', style: int = 1,
                 color: str = 'white', width: int = 1, plotindex: int = 0, valueaxisid: int = -1,
                 pricetick: float = -1.0, tickvalidmul: float = -1.0, showlegend: bool = True,
                 legendformat: str = '', legendcolor: str = '', bindinsid: str = '', bindrange: str = '', joinvalueaxis=True,
                 validmaxvalue: float = 9999999.99, validminvalue: float = -9999999.99, userdata: Dict[str, str] = {}):
        super().__init__(LineGraphParamDataPacker(self))
        self._ID: str = id
        self._Name: str = name
        if self._Name == '':
            self._Name = self._ID
        self._Style: int = style
        self._Color: str = color
        self._Width: int = width
        self._PlotIndex: int = plotindex
        self._ValueAxisID: int = valueaxisid
        self._PriceTick: float = pricetick
        self._TickValidMul: float = tickvalidmul
        self._ShowLegend: bool = showlegend
        self._LegendFormat: str = legendformat
        self._LegendColor: str = legendcolor
        self._BindInsID: str = bindinsid
        self._BindRange: str = bindrange
        self._JoinValueAxis: bool = joinvalueaxis
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
    def Style(self, value):
        self._Style = int(value)

    @property
    def Color(self):
        return self._Color

    @Color.setter
    def Color(self, value):
        self._Color = str(value)

    @property
    def Width(self):
        return self._Width

    @Width.setter
    def Width(self, value):
        self._Width = int(value)

    @property
    def PlotIndex(self):
        return self._PlotIndex

    @PlotIndex.setter
    def PlotIndex(self, value):
        self._PlotIndex = int(value)

    @property
    def ValueAxisID(self):
        return self._ValueAxisID

    @ValueAxisID.setter
    def ValueAxisID(self, value):
        self._ValueAxisID = int(value)

    @property
    def PriceTick(self):
        return self._PriceTick

    @PriceTick.setter
    def PriceTick(self, value):
        self._PriceTick = float(value)

    @property
    def TickValidMul(self):
        return self._TickValidMul

    @TickValidMul.setter
    def TickValidMul(self, value):
        self._TickValidMul = float(value)

    @property
    def ShowLegend(self):
        return self._ShowLegend

    @ShowLegend.setter
    def ShowLegend(self, value):
        self._ShowLegend = (value)

    @property
    def LegendFormat(self):
        return self._LegendFormat

    @LegendFormat.setter
    def LegendFormat(self, value):
        self._LegendFormat = str(value)

    @property
    def LegendColor(self):
        return self._LegendColor

    @LegendColor.setter
    def LegendColor(self, value):
        self._LegendColor = str(value)

    @property
    def BindInsID(self):
        return self._BindInsID

    @BindInsID.setter
    def BindInsID(self, value):
        self._BindInsID = str(value)

    @property
    def BindRange(self):
        return self._BindRange

    @BindRange.setter
    def BindRange(self, value):
        self._BindRange = str(value)

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
    def UserData(self):
        return self._UserData

    @UserData.setter
    def UserData(self, value: Dict[str, str]):
        self._UserData = value
