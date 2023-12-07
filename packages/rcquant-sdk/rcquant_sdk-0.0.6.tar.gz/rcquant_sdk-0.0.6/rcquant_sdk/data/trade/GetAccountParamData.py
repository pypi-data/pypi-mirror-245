from ...interface import IData
from ...data.trade.AccountData import AccountData
from ...packer.trade.GetAccountParamDataPacker import GetAccountParamDataPacker


class GetAccountParamData(IData):
    def __init__(self, tradename: str = ''):
        super().__init__(GetAccountParamDataPacker(self))
        self._TradeName = tradename
        self._Account: AccountData = AccountData()

    @property
    def TradeName(self):
        return self._TradeName

    @TradeName.setter
    def TradeName(self, value: str):
        self._TradeName = value

    @property
    def Account(self):
        return self._Account

    @Account.setter
    def Account(self, value: AccountData):
        self._Account: AccountData = value
