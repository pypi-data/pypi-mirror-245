# -*- coding: utf-8 -*-


# 店铺分服务
class StorescoreService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_operation_shop_growth(self, request):
        """
        查询店铺店铺分及待提升项
        :param request:查询条件
        """
        return self.__client.call("eleme.storeScore.queryOperationShopGrowth", {"request": request})

