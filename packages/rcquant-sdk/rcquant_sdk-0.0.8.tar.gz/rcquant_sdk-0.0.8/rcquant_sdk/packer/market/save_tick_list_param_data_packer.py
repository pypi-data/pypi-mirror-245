from ...interface import IPacker


class SaveTickListParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [
            self._obj.MarketName,
            self._obj.ExchangeID,
            self._obj.InstrumentID,
            self._obj.ProductID,
            self._obj.TradingDay,
            self._obj.PreClosePrice,
            self._obj.PreSettlementPrice,
            self._obj.PreOpenInterest,
            self._obj.UpperLimitPrice,
            self._obj.LowerLimitPrice,
            self._obj.ActionDayList,
            self._obj.TradingTimeList,
            self._obj.UpdateMillSecList,
            self._obj.LocalTimeList,
            self._obj.LastPriceList,
            self._obj.LastVolumeList,
            self._obj.BidPriceList,
            self._obj.BidVolumeList,
            self._obj.AskPriceList,
            self._obj.AskVolumeList,
            self._obj.AvgPriceList,
            self._obj.OpenPriceList,
            self._obj.HighPriceList,
            self._obj.LowerPriceList,
            self._obj.TotalTurnoverList,
            self._obj.TotalVolumeList,
            self._obj.OpenInterestList,
            self._obj.ClosePriceList,
            self._obj.SettlementPriceList,
            self._obj.TotalValueList
        ]

    def tuple_to_obj(self, t):
        if len(t) >= 30:
            self._obj.MarketName = t[0]
            self._obj.ExchangeID = t[1]
            self._obj.InstrumentID = t[2]
            self._obj.ProductID = t[3]
            self._obj.TradingDay = t[4]
            self._obj.PreClosePrice = t[5]
            self._obj.PreSettlementPrice = t[6]
            self._obj.PreOpenInterest = t[7]
            self._obj.UpperLimitPrice = t[8]
            self._obj.LowerLimitPrice = t[9]
            self._obj.ActionDayList = t[10]
            self._obj.TradingTimeList = t[11]
            self._obj.UpdateMillSecList = t[12]
            self._obj.LocalTimeList = t[13]
            self._obj.LastPriceList = t[14]
            self._obj.LastVolumeList = t[15]
            self._obj.BidPriceList = t[16]
            self._obj.BidVolumeList = t[17]
            self._obj.AskPriceList = t[18]
            self._obj.AskVolumeList = t[19]
            self._obj.AvgPriceList = t[20]
            self._obj.OpenPriceList = t[21]
            self._obj.HighPriceList = t[22]
            self._obj.LowerPriceList = t[23]
            self._obj.TotalTurnoverList = t[24]
            self._obj.TotalVolumeList = t[25]
            self._obj.OpenInterestList = t[26]
            self._obj.ClosePriceList = t[27]
            self._obj.SettlementPriceList = t[28]
            self._obj.TotalValueList = t[29]
            return True
        return False
