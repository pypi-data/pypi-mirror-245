# -*- coding: utf-8 -*-


# 订单服务
class CustomerorderService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_curr_mon_trade_info(self, request):
        """
        查询用户当前月订单信息
        :param request:手机号信息
        """
        return self.__client.call("eleme.customerOrder.queryCurrMonTradeInfo", {"request": request})

