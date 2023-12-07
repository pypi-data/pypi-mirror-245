from ...interface import IData
from ...packer.trade.PositionDataPacker import PositionDataPacker


class PositionData(IData):
    def __init__(self, investorid: str = '', brokerid: str = '', exchangeid: str = '', productid: str = '', instrumentid: str = '', instrumentname: str = '', deliverymonth: str = '', positionbuytoday: int = 0,
                 positionbuyyesterday: int = 0, positionbuy: int = 0, positionselltoday: int = 0, positionsellyesterday: int = 0, positionsell: int = 0, positiontotal: int = 0, canceledordercount: int = 0,
                 addordercount: int = 0, sumtradevolume: int = 0, selftradecount: int = 0, errorordercount: int = 0, buyopensum: int = 0, sellopensum: int = 0, buysum: int = 0, sellsum: int = 0,
                 buysumprice: float = 0, sellsumprice: float = 0, untradebuy: int = 0, untradesell: int = 0, untradeopen: int = 0, untradebuyopen: int = 0, untradesellopen: int = 0, untradeclose: int = 0,
                 untradebuyclose: int = 0, untradesellclose: int = 0, buyydposition: int = 0, sellydposition: int = 0, buypresettlementprice: float = 0.0, sellpresettlementprice: float = 0.0,
                 longavgprice: float = 0.0, shortavgprice: float = 0.0, frozenmargin: float = 0.0, longfrozenmargin: float = 0.0, shortfrozenmargin: float = 0.0, frozencommission: float = 0.0,
                 openfrozencommission: float = 0.0, closefrozencommission: float = 0.0, closetodayfrozencommission: float = 0.0, closeprofit: float = 0.0, longcloseprofit: float = 0.0,
                 shortcloseprofit: float = 0.0, currmargin: float = 0.0, longcurrmargin: float = 0.0, shortcurrmargin: float = 0.0, shortbasemargin: float = 0.0, shortposmargin: float = 0.0,
                 commission: float = 0.0, opencommission: float = 0.0, closecommission: float = 0.0, closetodaycommission: float = 0.0, positionprofit: float = 0.0, longpositionprofit: float = 0.0,
                 shortpositionprofit: float = 0.0, ordercommission: float = 0.0, royaltypositionprofit: float = 0.0, longroyaltypositionprofit: float = 0.0, shortroyaltypositionprofit: float = 0.0,
                 lockbuyopen: int = 0, lockbuyclose: int = 0, lockbuyclosetoday: int = 0, locksellopen: int = 0, locksellclose: int = 0, locksellclosetoday: int = 0):
        super().__init__(PositionDataPacker(self))
        self._InvestorID: str = investorid
        self._BrokerID: str = brokerid
        self._ExchangeID: str = exchangeid
        self._ProductID: str = productid
        self._InstrumentID: str = instrumentid
        self._InstrumentName: str = instrumentname
        self._DeliveryMonth: str = deliverymonth
        self._PositionBuyToday: int = positionbuytoday
        self._PositionBuyYesterday: int = positionbuyyesterday
        self._PositionBuy: int = positionbuy
        self._PositionSellToday: int = positionselltoday
        self._PositionSellYesterday: int = positionsellyesterday
        self._PositionSell: int = positionsell
        self._PositionTotal: int = positiontotal
        self._CanceledOrderCount: int = canceledordercount
        self._AddOrderCount: int = addordercount
        self._SumTradeVolume: int = sumtradevolume
        self._SelfTradeCount: int = selftradecount
        self._ErrorOrderCount: int = errorordercount
        self._BuyOpenSum: int = buyopensum
        self._SellOpenSum: int = sellopensum
        self._BuySum: int = buysum
        self._SellSum: int = sellsum
        self._BuySumPrice: float = buysumprice
        self._SellSumPrice: float = sellsumprice
        self._UnTradeBuy: int = untradebuy
        self._UnTradeSell: int = untradesell
        self._UntradeOpen: int = untradeopen
        self._UntradeBuyOpen: int = untradebuyopen
        self._UntradeSellOpen: int = untradesellopen
        self._UntradeClose: int = untradeclose
        self._UntradeBuyClose: int = untradebuyclose
        self._UntradeSellClose: int = untradesellclose
        self._BuyYdPosition: int = buyydposition
        self._SellYdPosition: int = sellydposition
        self._BuyPreSettlementPrice: float = buypresettlementprice
        self._SellPreSettlementPrice: float = sellpresettlementprice
        self._LongAvgPrice: float = longavgprice
        self._ShortAvgPrice: float = shortavgprice
        self._FrozenMargin: float = frozenmargin
        self._LongFrozenMargin: float = longfrozenmargin
        self._ShortFrozenMargin: float = shortfrozenmargin
        self._FrozenCommission: float = frozencommission
        self._OpenFrozenCommission: float = openfrozencommission
        self._CloseFrozenCommission: float = closefrozencommission
        self._CloseTodayFrozenCommission: float = closetodayfrozencommission
        self._CloseProfit: float = closeprofit
        self._LongCloseProfit: float = longcloseprofit
        self._ShortCloseProfit: float = shortcloseprofit
        self._CurrMargin: float = currmargin
        self._LongCurrMargin: float = longcurrmargin
        self._ShortCurrMargin: float = shortcurrmargin
        self._ShortBaseMargin: float = shortbasemargin
        self._ShortPosMargin: float = shortposmargin
        self._Commission: float = commission
        self._OpenCommission: float = opencommission
        self._CloseCommission: float = closecommission
        self._CloseTodayCommission: float = closetodaycommission
        self._PositionProfit: float = positionprofit
        self._LongPositionProfit: float = longpositionprofit
        self._ShortPositionProfit: float = shortpositionprofit
        self._OrderCommission: float = ordercommission
        self._RoyaltyPositionProfit: float = royaltypositionprofit
        self._LongRoyaltyPositionProfit: float = longroyaltypositionprofit
        self._ShortRoyaltyPositionProfit: float = shortroyaltypositionprofit
        self._LockBuyOpen: int = lockbuyopen
        self._LockBuyClose: int = lockbuyclose
        self._LockBuyCloseToday: int = lockbuyclosetoday
        self._LockSellOpen: int = locksellopen
        self._LockSellClose: int = locksellclose
        self._LockSellCloseToday: int = locksellclosetoday

    @property
    def InvestorID(self):
        return self._InvestorID

    @InvestorID.setter
    def InvestorID(self, value: str):
        self._InvestorID = value

    @property
    def BrokerID(self):
        return self._BrokerID

    @BrokerID.setter
    def BrokerID(self, value: str):
        self._BrokerID = value

    @property
    def ExchangeID(self):
        return self._ExchangeID

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        self._ExchangeID = value

    @property
    def ProductID(self):
        return self._ProductID

    @ProductID.setter
    def ProductID(self, value: str):
        self._ProductID = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def InstrumentName(self):
        return self._InstrumentName

    @InstrumentName.setter
    def InstrumentName(self, value: str):
        self._InstrumentName = value

    @property
    def DeliveryMonth(self):
        return self._DeliveryMonth

    @DeliveryMonth.setter
    def DeliveryMonth(self, value: str):
        self._DeliveryMonth = value

    @property
    def PositionBuyToday(self):
        return self._PositionBuyToday

    @PositionBuyToday.setter
    def PositionBuyToday(self, value: int):
        self._PositionBuyToday = value

    @property
    def PositionBuyYesterday(self):
        return self._PositionBuyYesterday

    @PositionBuyYesterday.setter
    def PositionBuyYesterday(self, value: int):
        self._PositionBuyYesterday = value

    @property
    def PositionBuy(self):
        return self._PositionBuy

    @PositionBuy.setter
    def PositionBuy(self, value: int):
        self._PositionBuy = value

    @property
    def PositionSellToday(self):
        return self._PositionSellToday

    @PositionSellToday.setter
    def PositionSellToday(self, value: int):
        self._PositionSellToday = value

    @property
    def PositionSellYesterday(self):
        return self._PositionSellYesterday

    @PositionSellYesterday.setter
    def PositionSellYesterday(self, value: int):
        self._PositionSellYesterday = value

    @property
    def PositionSell(self):
        return self._PositionSell

    @PositionSell.setter
    def PositionSell(self, value: int):
        self._PositionSell = value

    @property
    def PositionTotal(self):
        return self._PositionTotal

    @PositionTotal.setter
    def PositionTotal(self, value: int):
        self._PositionTotal = value

    @property
    def CanceledOrderCount(self):
        return self._CanceledOrderCount

    @CanceledOrderCount.setter
    def CanceledOrderCount(self, value: int):
        self._CanceledOrderCount = value

    @property
    def AddOrderCount(self):
        return self._AddOrderCount

    @AddOrderCount.setter
    def AddOrderCount(self, value: int):
        self._AddOrderCount = value

    @property
    def SumTradeVolume(self):
        return self._SumTradeVolume

    @SumTradeVolume.setter
    def SumTradeVolume(self, value: int):
        self._SumTradeVolume = value

    @property
    def SelfTradeCount(self):
        return self._SelfTradeCount

    @SelfTradeCount.setter
    def SelfTradeCount(self, value: int):
        self._SelfTradeCount = value

    @property
    def ErrorOrderCount(self):
        return self._ErrorOrderCount

    @ErrorOrderCount.setter
    def ErrorOrderCount(self, value: int):
        self._ErrorOrderCount = value

    @property
    def BuyOpenSum(self):
        return self._BuyOpenSum

    @BuyOpenSum.setter
    def BuyOpenSum(self, value: int):
        self._BuyOpenSum = value

    @property
    def SellOpenSum(self):
        return self._SellOpenSum

    @SellOpenSum.setter
    def SellOpenSum(self, value: int):
        self._SellOpenSum = value

    @property
    def BuySum(self):
        return self._BuySum

    @BuySum.setter
    def BuySum(self, value: int):
        self._BuySum = value

    @property
    def SellSum(self):
        return self._SellSum

    @SellSum.setter
    def SellSum(self, value: int):
        self._SellSum = value

    @property
    def BuySumPrice(self):
        return self._BuySumPrice

    @BuySumPrice.setter
    def BuySumPrice(self, value: float):
        self._BuySumPrice = value

    @property
    def SellSumPrice(self):
        return self._SellSumPrice

    @SellSumPrice.setter
    def SellSumPrice(self, value: float):
        self._SellSumPrice = value

    @property
    def UnTradeBuy(self):
        return self._UnTradeBuy

    @UnTradeBuy.setter
    def UnTradeBuy(self, value: int):
        self._UnTradeBuy = value

    @property
    def UnTradeSell(self):
        return self._UnTradeSell

    @UnTradeSell.setter
    def UnTradeSell(self, value: int):
        self._UnTradeSell = value

    @property
    def UntradeOpen(self):
        return self._UntradeOpen

    @UntradeOpen.setter
    def UntradeOpen(self, value: int):
        self._UntradeOpen = value

    @property
    def UntradeBuyOpen(self):
        return self._UntradeBuyOpen

    @UntradeBuyOpen.setter
    def UntradeBuyOpen(self, value: int):
        self._UntradeBuyOpen = value

    @property
    def UntradeSellOpen(self):
        return self._UntradeSellOpen

    @UntradeSellOpen.setter
    def UntradeSellOpen(self, value: int):
        self._UntradeSellOpen = value

    @property
    def UntradeClose(self):
        return self._UntradeClose

    @UntradeClose.setter
    def UntradeClose(self, value: int):
        self._UntradeClose = value

    @property
    def UntradeBuyClose(self):
        return self._UntradeBuyClose

    @UntradeBuyClose.setter
    def UntradeBuyClose(self, value: int):
        self._UntradeBuyClose = value

    @property
    def UntradeSellClose(self):
        return self._UntradeSellClose

    @UntradeSellClose.setter
    def UntradeSellClose(self, value: int):
        self._UntradeSellClose = value

    @property
    def BuyYdPosition(self):
        return self._BuyYdPosition

    @BuyYdPosition.setter
    def BuyYdPosition(self, value: int):
        self._BuyYdPosition = value

    @property
    def SellYdPosition(self):
        return self._SellYdPosition

    @SellYdPosition.setter
    def SellYdPosition(self, value: int):
        self._SellYdPosition = value

    @property
    def BuyPreSettlementPrice(self):
        return self._BuyPreSettlementPrice

    @BuyPreSettlementPrice.setter
    def BuyPreSettlementPrice(self, value: float):
        self._BuyPreSettlementPrice = value

    @property
    def SellPreSettlementPrice(self):
        return self._SellPreSettlementPrice

    @SellPreSettlementPrice.setter
    def SellPreSettlementPrice(self, value: float):
        self._SellPreSettlementPrice = value

    @property
    def LongAvgPrice(self):
        return self._LongAvgPrice

    @LongAvgPrice.setter
    def LongAvgPrice(self, value: float):
        self._LongAvgPrice = value

    @property
    def ShortAvgPrice(self):
        return self._ShortAvgPrice

    @ShortAvgPrice.setter
    def ShortAvgPrice(self, value: float):
        self._ShortAvgPrice = value

    @property
    def FrozenMargin(self):
        return self._FrozenMargin

    @FrozenMargin.setter
    def FrozenMargin(self, value: float):
        self._FrozenMargin = value

    @property
    def LongFrozenMargin(self):
        return self._LongFrozenMargin

    @LongFrozenMargin.setter
    def LongFrozenMargin(self, value: float):
        self._LongFrozenMargin = value

    @property
    def ShortFrozenMargin(self):
        return self._ShortFrozenMargin

    @ShortFrozenMargin.setter
    def ShortFrozenMargin(self, value: float):
        self._ShortFrozenMargin = value

    @property
    def FrozenCommission(self):
        return self._FrozenCommission

    @FrozenCommission.setter
    def FrozenCommission(self, value: float):
        self._FrozenCommission = value

    @property
    def OpenFrozenCommission(self):
        return self._OpenFrozenCommission

    @OpenFrozenCommission.setter
    def OpenFrozenCommission(self, value: float):
        self._OpenFrozenCommission = value

    @property
    def CloseFrozenCommission(self):
        return self._CloseFrozenCommission

    @CloseFrozenCommission.setter
    def CloseFrozenCommission(self, value: float):
        self._CloseFrozenCommission = value

    @property
    def CloseTodayFrozenCommission(self):
        return self._CloseTodayFrozenCommission

    @CloseTodayFrozenCommission.setter
    def CloseTodayFrozenCommission(self, value: float):
        self._CloseTodayFrozenCommission = value

    @property
    def CloseProfit(self):
        return self._CloseProfit

    @CloseProfit.setter
    def CloseProfit(self, value: float):
        self._CloseProfit = value

    @property
    def LongCloseProfit(self):
        return self._LongCloseProfit

    @LongCloseProfit.setter
    def LongCloseProfit(self, value: float):
        self._LongCloseProfit = value

    @property
    def ShortCloseProfit(self):
        return self._ShortCloseProfit

    @ShortCloseProfit.setter
    def ShortCloseProfit(self, value: float):
        self._ShortCloseProfit = value

    @property
    def CurrMargin(self):
        return self._CurrMargin

    @CurrMargin.setter
    def CurrMargin(self, value: float):
        self._CurrMargin = value

    @property
    def LongCurrMargin(self):
        return self._LongCurrMargin

    @LongCurrMargin.setter
    def LongCurrMargin(self, value: float):
        self._LongCurrMargin = value

    @property
    def ShortCurrMargin(self):
        return self._ShortCurrMargin

    @ShortCurrMargin.setter
    def ShortCurrMargin(self, value: float):
        self._ShortCurrMargin = value

    @property
    def ShortBaseMargin(self):
        return self._ShortBaseMargin

    @ShortBaseMargin.setter
    def ShortBaseMargin(self, value: float):
        self._ShortBaseMargin = value

    @property
    def ShortPosMargin(self):
        return self._ShortPosMargin

    @ShortPosMargin.setter
    def ShortPosMargin(self, value: float):
        self._ShortPosMargin = value

    @property
    def Commission(self):
        return self._Commission

    @Commission.setter
    def Commission(self, value: float):
        self._Commission = value

    @property
    def OpenCommission(self):
        return self._OpenCommission

    @OpenCommission.setter
    def OpenCommission(self, value: float):
        self._OpenCommission = value

    @property
    def CloseCommission(self):
        return self._CloseCommission

    @CloseCommission.setter
    def CloseCommission(self, value: float):
        self._CloseCommission = value

    @property
    def CloseTodayCommission(self):
        return self._CloseTodayCommission

    @CloseTodayCommission.setter
    def CloseTodayCommission(self, value: float):
        self._CloseTodayCommission = value

    @property
    def PositionProfit(self):
        return self._PositionProfit

    @PositionProfit.setter
    def PositionProfit(self, value: float):
        self._PositionProfit = value

    @property
    def LongPositionProfit(self):
        return self._LongPositionProfit

    @LongPositionProfit.setter
    def LongPositionProfit(self, value: float):
        self._LongPositionProfit = value

    @property
    def ShortPositionProfit(self):
        return self._ShortPositionProfit

    @ShortPositionProfit.setter
    def ShortPositionProfit(self, value: float):
        self._ShortPositionProfit = value

    @property
    def OrderCommission(self):
        return self._OrderCommission

    @OrderCommission.setter
    def OrderCommission(self, value: float):
        self._OrderCommission = value

    @property
    def RoyaltyPositionProfit(self):
        return self._RoyaltyPositionProfit

    @RoyaltyPositionProfit.setter
    def RoyaltyPositionProfit(self, value: float):
        self._RoyaltyPositionProfit = value

    @property
    def LongRoyaltyPositionProfit(self):
        return self._LongRoyaltyPositionProfit

    @LongRoyaltyPositionProfit.setter
    def LongRoyaltyPositionProfit(self, value: float):
        self._LongRoyaltyPositionProfit = value

    @property
    def ShortRoyaltyPositionProfit(self):
        return self._ShortRoyaltyPositionProfit

    @ShortRoyaltyPositionProfit.setter
    def ShortRoyaltyPositionProfit(self, value: float):
        self._ShortRoyaltyPositionProfit = value

    @property
    def LockBuyOpen(self):
        return self._LockBuyOpen

    @LockBuyOpen.setter
    def LockBuyOpen(self, value: int):
        self._LockBuyOpen = value

    @property
    def LockBuyClose(self):
        return self._LockBuyClose

    @LockBuyClose.setter
    def LockBuyClose(self, value: int):
        self._LockBuyClose = value

    @property
    def LockBuyCloseToday(self):
        return self._LockBuyCloseToday

    @LockBuyCloseToday.setter
    def LockBuyCloseToday(self, value: int):
        self._LockBuyCloseToday = value

    @property
    def LockSellOpen(self):
        return self._LockSellOpen

    @LockSellOpen.setter
    def LockSellOpen(self, value: int):
        self._LockSellOpen = value

    @property
    def LockSellClose(self):
        return self._LockSellClose

    @LockSellClose.setter
    def LockSellClose(self, value: int):
        self._LockSellClose = value

    @property
    def LockSellCloseToday(self):
        return self._LockSellCloseToday

    @LockSellCloseToday.setter
    def LockSellCloseToday(self, value: int):
        self._LockSellCloseToday = value
