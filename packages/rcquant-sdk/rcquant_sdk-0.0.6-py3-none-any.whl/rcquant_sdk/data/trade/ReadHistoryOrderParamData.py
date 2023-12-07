from typing import List
from ...interface import IData
from ...packer.trade.ReadHistoryOrderParamDataPacker import ReadHistoryOrderParamDataPacker
from ...data.trade.OrderData import OrderData


class ReadHistoryOrderParamData(IData):
    def __init__(self, startdate: str = '', enddate: str = '', datalist: List[OrderData] = []):
        super().__init__(ReadHistoryOrderParamDataPacker(self))
        self._StartDate: str = startdate
        self._EndDate: str = enddate
        self._DataList: List[OrderData] = datalist

    @property
    def StartDate(self):
        return self._StartDate

    @StartDate.setter
    def StartDate(self, value: str):
        self._StartDate = value

    @property
    def EndDate(self):
        return self._EndDate

    @EndDate.setter
    def EndDate(self, value: str):
        self._EndDate = value

    @property
    def DataList(self):
        return self._DataList

    @DataList.setter
    def DataList(self, value: List[OrderData]):
        self._DataList = value
