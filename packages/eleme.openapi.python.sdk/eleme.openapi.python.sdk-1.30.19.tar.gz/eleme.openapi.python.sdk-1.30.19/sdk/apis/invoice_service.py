# -*- coding: utf-8 -*-


# 发票服务
class InvoiceService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def batch_query_shop_settings(self, request):
        """
        批量查询店铺开票设置
        :param request:查询请求
        """
        return self.__client.call("eleme.invoice.seller.batchQueryShopSettings", {"request": request})

    def batch_update_shop_settings(self, request):
        """
        批量更新店铺开票设置
        :param request:更新请求
        """
        return self.__client.call("eleme.invoice.seller.batchUpdateShopSettings", {"request": request})

    def batch_query_shop_application(self, request):
        """
        批量查询店铺开票申请
        :param request:查询请求
        """
        return self.__client.call("eleme.invoice.seller.batchQueryShopApplication", {"request": request})

    def batch_update_shop_application(self, request):
        """
        批量更新店铺开票申请
        :param request:更新请求
        """
        return self.__client.call("eleme.invoice.seller.batchUpdateShopApplication", {"request": request})

