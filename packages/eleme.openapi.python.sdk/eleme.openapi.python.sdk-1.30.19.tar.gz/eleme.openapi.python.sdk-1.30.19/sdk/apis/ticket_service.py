# -*- coding: utf-8 -*-


# 小票服务
class TicketService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def create_ticket_token(self, ticket_token_request):
        """
        创建小票设置页面token
        :param ticketTokenRequest:创建小票token信息
        """
        return self.__client.call("eleme.ticket.createTicketToken", {"ticketTokenRequest": ticket_token_request})

    def query_print_settings(self, shop_id):
        """
        根据店铺id获取店铺小票打印联配置数据
        :param shopId:店铺ID
        """
        return self.__client.call("eleme.ticket.queryPrintSettings", {"shopId": shop_id})

    def update_print_settings(self, request):
        """
        根据店铺id修改店铺小票打印联配置数据
        :param request:打印联设置
        """
        return self.__client.call("eleme.ticket.updatePrintSettings", {"request": request})

    def get_test_ticket_data(self, shop_id, ticket_type):
        """
        打印测试小票
        :param shopId:店铺ID
        :param ticketType:打印联信息
        """
        return self.__client.call("eleme.ticket.getTestTicketData", {"shopId": shop_id, "ticketType": ticket_type})

    def get_ticket_data_for_pull(self, request):
        """
        小票补打接口
        :param request:小票补打信息
        """
        return self.__client.call("eleme.ticket.getTicketDataForPull", {"request": request})

