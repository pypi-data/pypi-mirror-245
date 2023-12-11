from typing import Dict
from ...interface import IData
from ...packer.chart.text_graph_param_data_packer import TextGraphParamDataPacker


class TextGraphParamData(IData):
    def __init__(self, id: str = '', name: str = '', color: str = 'white', plot_index: int = 0, value_axis_id: int = -1,
                 text: str = '', key: float = 0.0, value: float = 0.0, mill_ts: int = -1, join_value_axis=True, user_data: Dict[str, str] = {}):
        super().__init__(TextGraphParamDataPacker(self))
        self._ID = id
        self._Name = name
        self._Color = color
        self._PlotIndex = plot_index
        self._ValueAxisID = value_axis_id
        self._Text = text
        self._Key = key
        self._Value = value
        self._MillTimeSpan = mill_ts
        self._JoinValueAxis: bool = join_value_axis
        self._UserData: Dict[str, str] = user_data

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
    def Color(self):
        return self._Color

    @Color.setter
    def Color(self, value: str):
        self._Color = value

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
    def Text(self):
        return self._Text

    @Text.setter
    def Text(self, value: str):
        self._Text = value

    @property
    def Key(self):
        return self._Key

    @Key.setter
    def Key(self, value: float):
        self._Key = value

    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, value: float):
        self._Value = value

    @property
    def MillTimeSpan(self):
        return self._MillTimeSpan

    @MillTimeSpan.setter
    def MillTimeSpan(self, value: int):
        self._MillTimeSpan = value

    @property
    def JoinValueAxis(self):
        return self._JoinValueAxis

    @JoinValueAxis.setter
    def JoinValueAxis(self, value: bool):
        self._JoinValueAxis = value

    @property
    def UserData(self):
        return self._UserData

    @UserData.setter
    def UserData(self, value: Dict[str, str]):
        self._UserData = value
