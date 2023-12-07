from ...interface import IData
from ...packer.chart.TimeAxisParamDataPacker import TimeAxisParamDataPacker


class TimeAxisParamData(IData):
    def __init__(self, showlabels: str = '', format: str = ''):
        super().__init__(TimeAxisParamDataPacker(self))
        self._ShowLabels: str = showlabels
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
