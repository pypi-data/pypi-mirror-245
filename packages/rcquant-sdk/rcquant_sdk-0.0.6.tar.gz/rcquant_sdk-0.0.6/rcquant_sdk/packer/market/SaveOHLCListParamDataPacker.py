from ...interface import IPacker


class SaveOHLCListParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [
            self._obj.MarketName,
            self._obj.ExchangeID,
            self._obj.InstrumentID,
            self._obj.Range,
            self._obj.TradingDay,
            self._obj.ActionDay,
            self._obj.PreSettlementPrice,
            self._obj.ActionTimespanList,
            self._obj.TradingTimeList,
            self._obj.StartTimeList,
            self._obj.EndTimeList,
            self._obj.TotalTurnoverList,
            self._obj.OpenInterestList,
            self._obj.OpenPriceList,
            self._obj.OpenBidPriceList,
            self._obj.OpenAskPriceList,
            self._obj.OpenBidVolumeList,
            self._obj.OpenAskVolumeList,
            self._obj.HighPriceList,
            self._obj.HighBidPriceList,
            self._obj.HighAskPriceList,
            self._obj.HighBidVolumeList,
            self._obj.HighAskVolumeList,
            self._obj.LowerPriceList,
            self._obj.LowerBidPriceList,
            self._obj.LowerAskPriceList,
            self._obj.LowerBidVolumeList,
            self._obj.LowerAskVolumeList,
            self._obj.ClosePriceList,
            self._obj.CloseBidPriceList,
            self._obj.CloseAskPriceList,
            self._obj.CloseBidVolumeList,
            self._obj.CloseAskVolumeList
        ]

    def tuple_to_obj(self, t):
        if len(t) >= 33:
            self._obj.MarketName = t[0]
            self._obj.ExchangeID = t[1]
            self._obj.InstrumentID = t[2]
            self._obj.Range = t[3]
            self._obj.TradingDay = t[4]
            self._obj.ActionDay = t[5]
            self._obj.PreSettlementPrice = t[6]
            self._obj.ActionTimespanList = t[7]
            self._obj.TradingTimeList = t[8]
            self._obj.StartTimeList = t[9]
            self._obj.EndTimeList = t[10]
            self._obj.TotalTurnoverList = t[11]
            self._obj.OpenInterestList = t[12]
            self._obj.OpenPriceList = t[13]
            self._obj.OpenBidPriceList = t[14]
            self._obj.OpenAskPriceList = t[15]
            self._obj.OpenBidVolumeList = t[16]
            self._obj.OpenAskVolumeList = t[17]
            self._obj.HighPriceList = t[18]
            self._obj.HighBidPriceList = t[19]
            self._obj.HighAskPriceList = t[20]
            self._obj.HighBidVolumeList = t[21]
            self._obj.HighAskVolumeList = t[22]
            self._obj.LowerPriceList = t[23]
            self._obj.LowerBidPriceList = t[24]
            self._obj.LowerAskPriceList = t[25]
            self._obj.LowerBidVolumeList = t[26]
            self._obj.LowerAskVolumeList = t[27]
            self._obj.ClosePriceList = t[28]
            self._obj.CloseBidPriceList = t[29]
            self._obj.CloseAskPriceList = t[30]
            self._obj.CloseBidVolumeList = t[31]
            self._obj.CloseAskVolumeList = t[32]
            return True
        return False
