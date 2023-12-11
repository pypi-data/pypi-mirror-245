from ...interface import IData
from ...packer.chart.plot_param_data_packer import PlotParamDataPacker


class PlotParamData(IData):
    def __init__(self, plot_index: int = 0, plot_name: str = '', plot_name_color: str = 'white', height: int = 100,
                 is_eqvalue_axis: bool = True, grid_style: int = 2, grid_color: str = "#323232", back_ground_color: str = "black",
                 border_color: str = "red", border_width: int = 1, show_legend_item: bool = True, grid_x_style: int = 2, grid_x_color: str = '#323232'):
        super().__init__(PlotParamDataPacker(self))
        self._PlotIndex: int = plot_index
        self._Height: int = height
        self._IsEqValueAxis: bool = is_eqvalue_axis
        self._GridStyle: int = grid_style
        self._GridColor: str = grid_color
        self._BackGroundColor: str = back_ground_color
        self._BorderColor: str = border_color
        self._BorderWidth: int = border_width
        self._ShowLegendItem: bool = show_legend_item
        self._PlotName: str = plot_name
        self._PlotNameColor: str = plot_name_color
        self._GridXColor: str = grid_x_color
        self._GridXStyle: int = grid_x_style

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
