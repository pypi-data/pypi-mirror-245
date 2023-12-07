# -*- coding: utf-8 -*-


# 卡券订单服务（对外提供）
class CouponService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_coupon_order(self, request):
        """
        查询卡券订单信息
        :param request:查询条件
        """
        return self.__client.call("eleme.coupon.queryCouponOrder", {"request": request})

