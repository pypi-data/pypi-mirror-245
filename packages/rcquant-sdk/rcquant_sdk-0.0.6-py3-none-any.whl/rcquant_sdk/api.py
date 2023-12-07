from typing import List, Dict, Tuple
from .client import FinClient
from .data.LoginData import LoginData
from .data.market.OHLCData import OHLCData
from .data.chart.ChartInitParamData import ChartInitParamData
from .data.chart.MarkerGraphParamData import MarkerGraphParamData
from .data.chart.TextGraphParamData import TextGraphParamData
from .data.chart.FinancialGraphParamData import FinancialGraphParamData
from .data.chart.LineGraphParamData import LineGraphParamData
from .data.chart.OHLCValueData import OHLCValueData
from .data.chart.GraphValueData import GraphValueData
from .data.trade.OrderData import OrderData
from .data.market.MarketParamData import MarketParamData
from .data.market.QueryParamData import QueryParamData
from .data.market.SubOHLCParamData import SubOHLCParamData
from .data.market.HistoryOHLCParamData import HistoryOHLCParamData
from .data.market.SaveOHLCListParamData import SaveOHLCListParamData
from .data.trade.TradeParamData import TradeParamData
from .data.trade.ReadHistoryOrderParamData import ReadHistoryOrderParamData
from .data.trade.ReadHistoryTradeOrderParamData import ReadHistoryTradeOrderParamData
from .data.trade.GetAccountParamData import GetAccountParamData
from .data.trade.GetOrdersParamData import GetOrdersParamData
from .data.trade.GetTradeOrdersParamData import GetTradeOrdersParamData
from .data.trade.GetPositionsParamData import GetPositionsParamData
from .data.chart.BarGraphParamData import BarGraphParamData


def conncet(host: str = None, port: str = None, ):
    return FinClient.instance().connect(host, port)


def login(user_id: str = '', password: str = ''):
    return FinClient.instance().base_handle().login(LoginData(user_id, password))


def close():
    FinClient.instance().close()


def set_callback(**kwargs):
    '''
    设置行情回调
    :param kwargs OnTick=None,
    '''
    FinClient.instance().set_callback(**kwargs)


def set_auth_params(userid, password, host=None, port=None):
    '''
    设置登录信息
    :param userid:用户名
    :param password:密码
    :param host:网络地址默认为None
    :param port:端口号默认为None
    :return:result msg
    '''
    ret = conncet(host, port)
    if ret is None or ret[0] is False:
        return ret
    return login(userid, password)


def set_chart_init_params(params: ChartInitParamData):
    return FinClient.instance().chart_handle().set_chart_init_params(params)


def add_line_graph(id: str, plotindex=0, yaxisid=-1, color: str = '#FFF', style=0, valtick=0.01, validmul=-1.0, bindinsid='', bindrange=''):
    '''
    添加线图
    :param id:图形ID
    :param plotindex:所在图层索引
    :param yaxisid:所属Y轴
    :param color:颜色
    :param style:样式
    :param valtick:最小变动刻度
    :param vallen:
    :param validmul:显示有效的倍数 -1.0不做限制
    :param bindinsid:绑定合约
    :param bindrange:绑定合约周期
    :return:result msg
    '''
    return FinClient.instance().chart_handle().add_line_graph(
        LineGraphParamData(
            name=id,
            id=id,
            plotindex=plotindex,
            valueaxisid=yaxisid,
            style=style,
            color=color,
            pricetick=valtick,
            tickvalidmul=validmul,
            bindinsid=bindinsid,
            bindrange=bindrange)
    )


def add_bar_graph(id: str, plotindex=0, yaxisid=-1, color: str = '#FFF', style=0, framestyle=2):
    '''
    添加柱状图
    :param id:图形id
    :param plotindex:所在图层索引
    :param yaxisid:所属Y轴
    :param color:颜色
    :param style:样式
    :param framestyle:边框样式
    :return:result msg
    '''
    return FinClient.instance().chart_handle().add_bar_graph(
        BarGraphParamData(
            name=id,
            id=id,
            plotindex=plotindex,
            valueaxis_id=yaxisid,
            style=style,
            framestyle=framestyle,
            color=color,
        )
    )


def add_financial_graph(id: str, plotindex=0, yaxisid=-1, color: str = '', style=0, valtick=0.01, vallen=6.0, validmul=-1.0, bindinsid='', bindrange=''):
    '''
    添加线图
    :param graph_name:图形名称
    :param plot_index:所在图层索引
    :param yaxisid:所属Y轴
    :param color:颜色
    :param style:样式
    :param valtick:最小变动刻度
    :param vallen:
    :param validmul:显示有效的倍数 -1.0不做限制
    :param bindinsid:绑定合约
    :param bindrange:绑定合约周期
    :return:result msg
    '''
    return FinClient.instance().chart_handle().add_financial_graph(
        FinancialGraphParamData(
            id=id,
            name=id,
            style=style,
            plotindex=plotindex,
            valueaxisid=yaxisid,
            pricetick=valtick,
            tickvalidmul=validmul,
            bindinsid=bindinsid,
            bindrange=bindrange)
    )


def chart_init_show():
    return FinClient.instance().chart_handle().chart_init_show()


def add_line_value(graphid: str, key: float = 0.0, value: float = 0.0, millts: int = -1):
    return FinClient.instance().chart_handle().add_graph_value(GraphValueData(
        graphid=graphid,
        key=key,
        millts=millts,
        value=value)
    )


def add_marker_graph(param: MarkerGraphParamData):
    return FinClient.instance().chart_handle().add_marker_graph(param)


def add_graph_value(gv: GraphValueData):
    return FinClient.instance().chart_handle().add_graph_value(gv)


def add_graph_value_list(gvl):
    gvdl = []
    for gv in gvl:
        gvdl.append(GraphValueData(graphid=gv[0], millts=gv[1], value=gv[2]))
    return FinClient.instance().chart_handle().add_graph_value_list(gvdl)


def add_timespan_graphvalue_list(timespans: List[int], graphvalues: Dict[str, List[float]] = {}, ohlcvalues: Dict[str, Tuple[List[float], List[float], List[float], List[float]]] = {}):
    return FinClient.instance().chart_handle().add_timespan_graphvalue_list(timespans, graphvalues, ohlcvalues)


def add_ohlc_value(ov: OHLCValueData):
    return FinClient.instance().chart_handle().add_ohlc_value(ov)


def add_ohlc_value_list(ovl: List[OHLCValueData]):
    return FinClient.instance().chart_handle().add_ohlc_value_list(ovl)


def add_ohlc(graphid: str, o: OHLCData):
    '''
    添加OHLC值
    :param graphid:图形名称
    :param o:ohlc
    :return:result,msg
    '''
    return FinClient.instance().chart_handle().add_ohlc_value(
        OHLCValueData(
            graphid=graphid,
            ohlcdata=o)
    )


def draw_text(pindex: int, yaxisid: int, key: float, value: float, text: str, color: str = '#FFF'):
    '''
    画文本
    :param plot_index:所在图层索引
    :param yaxisid:所属Y轴
    :param key:x轴值
    :param value:y轴值
    :param text:文本
    :param color:颜色
    :return:result,msg
    '''
    return FinClient.instance().chart_handle().add_text_graph(
        TextGraphParamData(
            plotindex=pindex,
            valueaxisid=yaxisid,
            key=key,
            value=value,
            text=text,
            color=color)
    )


def add_text_graph(param: TextGraphParamData):
    return FinClient.instance().chart_handle().add_text_graph(param)


def draw_text_milltime(pindex, yaxisid, millts, value, text, color='#FFF'):
    '''
    画文本
    :param plot_index:所在图层索引
    :param yaxisid:所属Y轴
    :param millts:x时间戳
    :param value:y轴值
    :param text:文本
    :param color:颜色
    :return:result,msg
    '''
    return FinClient.instance().chart_handle().add_text_graph(
        TextGraphParamData(
            plot_index=pindex,
            value_axis_id=yaxisid,
            mill_ts=millts,
            value=value,
            text=text,
            color=color)
    )


def set_market_params(market_names):
    '''
    设置行情参数
    :param market_names:行情名称多个时候用逗号分隔
    :return:result,msg
    '''
    return FinClient.instance().market_handle().set_market_params(
        MarketParamData(marketnames=market_names)
    )


def subscribe(market_name: str, exchangid: str, instrumentid: str):
    '''
    订阅行情
    :param market_name:行情名称
    :param exchangid:交易所编码
    :param instrumentid:合约编码
    :return:result,msg
    '''
    return FinClient.instance().market_handle().subscribe(
        QueryParamData(
            marketname=market_name,
            exchangeid=exchangid,
            instrumentid=instrumentid)
    )


def subscribe_ohlc(market_name: str, exchangid: str, instrumentid: str, range: str):
    '''
    订阅行情
    :param market_name:行情名称
    :param exchangid:交易所编码
    :param instrumentid:合约编码
    :param range:周期
    :return:result,msg
    '''
    return FinClient.instance().market_handle().subscribe_ohlc(
        SubOHLCParamData(
            marketname=market_name,
            exchangeid=exchangid,
            instrumentid=instrumentid,
            range=range)
    )


def get_history_ohlc(marketname: str, exchangid: str, instrumentid: str, range: str, startdate: str, enddate: str, isreturnlist: bool = False):
    '''
    获取历史ohlc数据
    :param market_name:行情名称
    :param exchangid:交易所编码
    :param instrumentid:合约编码
    :param range:周期
    :param start_date 开始日期
    :param end_date 结束日期
    :param isreturnlist 是否返回list格式
    :return:result,msg
    '''
    return FinClient.instance().market_handle().get_history_ohlc(
        HistoryOHLCParamData(
            marketname=marketname,
            exchangeid=exchangid,
            instrumentid=instrumentid,
            range=range,
            startdate=startdate,
            enddate=enddate,
            isreturnlist=isreturnlist)
    )


def save_ohlc_list(
    marketname: str = '',
    exchangeid: str = '',
    instrumentid: str = '',
    range: int = 60,
    tradingday: str = '',
    actionday: str = '',
    presettlementprice: float = 0.0,
    actiontimespanlist: List[int] = [],
    tradingtimelist: List[str] = [],
    starttimelist: List[str] = [],
    endtimelist: List[str] = [],
    totalturnoverlist: List[float] = [],
    openinterestlist: List[float] = [],
    openpricelist: List[float] = [],
    openbidpricelist: List[float] = [],
    openaskpricelist: List[float] = [],
    openbidvolumelist: List[int] = [],
    openaskvolumelist: List[int] = [],
    highpricelist: List[float] = [],
    highbidpricelist: List[float] = [],
    highaskpricelist: List[float] = [],
    highbidvolumelist: List[int] = [],
    highaskvolumelist: List[int] = [],
    lowerpricelist: List[float] = [],
    lowerbidpricelist: List[float] = [],
    loweraskpricelist: List[float] = [],
    lowerbidvolumelist: List[int] = [],
    loweraskvolumelist: List[int] = [],
    closepricelist: List[float] = [],
    closebidpricelist: List[float] = [],
    closeaskpricelist: List[float] = [],
    closebidvolumelist: List[int] = [],
    closeaskvolumelist: List[int] = []
):
    return FinClient.instance().market_handle().save_ohlc_list(
        SaveOHLCListParamData(marketname=marketname,
                              exchangeid=exchangeid,
                              instrumentid=instrumentid,
                              range=range,
                              tradingday=tradingday,
                              actionday=actionday,
                              presettlementprice=presettlementprice,
                              actiontimespanlist=actiontimespanlist,
                              tradingtimelist=tradingtimelist,
                              starttimelist=starttimelist,
                              endtimelist=endtimelist,
                              totalturnoverlist=totalturnoverlist,
                              openinterestlist=openinterestlist,
                              openpricelist=openpricelist,
                              openbidpricelist=openbidpricelist,
                              openaskpricelist=openaskpricelist,
                              openbidvolumelist=openbidvolumelist,
                              openaskvolumelist=openaskvolumelist,
                              highpricelist=highpricelist,
                              highbidpricelist=highbidpricelist,
                              highaskpricelist=highaskpricelist,
                              highbidvolumelist=highbidvolumelist,
                              highaskvolumelist=highaskvolumelist,
                              lowerpricelist=lowerpricelist,
                              lowerbidpricelist=lowerbidpricelist,
                              loweraskpricelist=loweraskpricelist,
                              lowerbidvolumelist=lowerbidvolumelist,
                              loweraskvolumelist=loweraskvolumelist,
                              closepricelist=closepricelist,
                              closebidpricelist=closebidpricelist,
                              closeaskpricelist=closeaskpricelist,
                              closebidvolumelist=closebidvolumelist,
                              closeaskvolumelist=closeaskvolumelist)
    )


def set_trade_params(tradenames: str):
    return FinClient.instance().trade_handle().set_trade_params(
        TradeParamData(
            tradenames=tradenames)
    )


def insert_order(tradename, excid: str, insid: str, direc: int, price: float, vol: int, openclose: int):
    return FinClient.instance().trade_handle().insert_order(
        OrderData(
            exchangeid=excid,
            instrumentid=insid,
            price=price,
            direction=direc,
            volume=vol,
            investorid=tradename,
            openclosetype=openclose
        )
    )


def cancel_order_by_data(order: OrderData):
    return FinClient.instance().trade_handle().cancel_order(order)


def cancel_order(tradename: str, orderid: str, instrumentid: str, orderref: str, price: float):
    return FinClient.instance().trade_handle().cancel_order(
        OrderData(
            investorid=tradename,
            orderid=orderid,
            instrumentid=instrumentid,
            orderref=orderref,
            price=price
        )
    )


def read_history_orders(startdate: str, enddate):
    return FinClient.instance().trade_handle().read_history_orders(
        ReadHistoryOrderParamData(
            startdate=startdate,
            enddate=enddate
        )
    )


def read_history_tradeorders(startdate: str, enddate):
    return FinClient.instance().trade_handle().read_history_tradeorders(
        ReadHistoryTradeOrderParamData(
            startdate=startdate,
            enddate=enddate
        )
    )


def get_orders(tradename: str):
    return FinClient.instance().trade_handle().get_orders(
        GetOrdersParamData(
            tradename=tradename
        )
    )


def get_tradeorders(tradename: str):
    return FinClient.instance().trade_handle().get_tradeorders(
        GetTradeOrdersParamData(
            tradename=tradename
        )
    )


def get_positions(tradename: str):
    return FinClient.instance().trade_handle().get_positions(
        GetPositionsParamData(
            tradename=tradename
        )
    )


def get_account(tradename: str):
    return FinClient.instance().trade_handle().get_account(
        GetAccountParamData(
            tradename=tradename
        )
    )


def save_chart_data(filename: str):
    return FinClient.instance().chart_handle().save_chart_data(filename)


def load_chart_data(filename: str):
    return FinClient.instance().chart_handle().load_chart_data(filename)
