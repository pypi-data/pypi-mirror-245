from typing import List, Dict, Tuple
from ...interface import IData
from ...packer.chart.TimeSpanGVListDataPacker import TimeSpanGVListDataPacker


class TimeSpanGVListData(IData):
    def __init__(self, timespans: List[int], graphvalues: Dict[str, List[float]] = {},
                 ohlcvalues: Dict[str, Tuple[List[float], List[float], List[float], List[float]]] = {}):
        super().__init__(TimeSpanGVListDataPacker(self))
        if timespans is None:
            timespans = []
        self._TimeSpanList: List[int] = timespans
        if graphvalues is None:
            graphvalues = {}
        self._GraphValueList: Dict[str, List[float]] = graphvalues
        if ohlcvalues is None:
            ohlcvalues = {}
        self._OHLCValueList: Dict[str, Tuple[List[float], List[float], List[float], List[float]]] = ohlcvalues

    @ property
    def TimeSpanList(self):
        return self._TimeSpanList

    @ TimeSpanList.setter
    def TimeSpanList(self, value: List[int]):
        self._TimeSpanList = value

    @ property
    def GraphValueList(self):
        return self._GraphValueList

    @ GraphValueList.setter
    def GraphValueList(self, value: Dict[str, List[float]]):
        self._GraphValueList = value

    @ property
    def OHLCValueList(self):
        return self._OHLCValueList

    @ OHLCValueList.setter
    def OHLCValueList(self, value: Dict[str, Tuple[List[float], List[float], List[float], List[float]]]):
        self._OHLCValueList = value
