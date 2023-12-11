from ...interface import IData
from ...packer.chart.time_axis_param_data_packer import TimeAxisParamDataPacker


class TimeAxisParamData(IData):
    def __init__(self, show_labels: str = '', format: str = ''):
        super().__init__(TimeAxisParamDataPacker(self))
        self._ShowLabels: str = show_labels
        self._Format: str = format

    @property
    def ShowLabels(self):
        return self._ShowLabels

    @ShowLabels.setter
    def ShowLabels(self, value: str):
        self._ShowLabels = value

    @property
    def Format(self):
        return self._Format

    @Format.setter
    def Format(self, value: str):
        self._Format = value
