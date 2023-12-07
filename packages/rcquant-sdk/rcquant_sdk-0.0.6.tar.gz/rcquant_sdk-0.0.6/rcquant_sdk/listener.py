from abc import abstractmethod
from .data.market.TickData import TickData
from .data.market.OHLCData import OHLCData
from .data.trade.OrderData import OrderData
from .data.trade.TradeOrderData import TradeOrderData


class IListener(object):

    @abstractmethod
    def on_connect(self):
        pass

    @abstractmethod
    def on_disconnect(self):
        pass

    @abstractmethod
    def on_tick(self, tick: TickData):
        pass

    @abstractmethod
    def on_ohlc(self, ohlc: OHLCData):
        pass

    @abstractmethod
    def on_order_update(self, order: OrderData):
        pass

    @abstractmethod
    def on_tradeorder_update(self, tradeorder: TradeOrderData):
        pass
