# -*- coding: utf-8 -*-


# 生意参谋服务
class CanmouService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_shop_realtime_overview(self, request):
        """
        查询实时店铺总览数据
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryShopRealtimeOverview", {"request": request})

    def query_shop_realtime_flow(self, request):
        """
        查询实时店铺流量数据
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryShopRealtimeFlow", {"request": request})

    def query_shop_realtime_item(self, request):
        """
        分页查询实时店铺商品数据
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryShopRealtimeItem", {"request": request})

    def query_shop_history_item(self, request):
        """
        分页查询近30天店铺商品数据
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryShopHistoryItem", {"request": request})

    def query_shop_item_rank(self, request):
        """
        查询近30天店铺热销商品排行
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryShopItemRank", {"request": request})

    def query_market_realtime_flow(self, request):
        """
        查询实时商圈流量数据
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryMarketRealtimeFlow", {"request": request})

    def query_market_item(self, request):
        """
        查询近30天商圈热销商品排行
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryMarketItem", {"request": request})

    def query_market_shop_sale(self, request):
        """
        查询近30天商圈同品类门店月售
        :param request:查询条件
        """
        return self.__client.call("eleme.canmou.queryMarketShopSale", {"request": request})

