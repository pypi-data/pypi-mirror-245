# -*- coding: utf-8 -*-


# 金融服务
class FinanceService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_new_balance(self, shop_id):
        """
        查询商户余额 返回可用余额和子账户余额明细
        :param shopId:饿了么总店店铺id
        """
        return self.__client.call("eleme.finance.queryNewBalance", {"shopId": shop_id})

    def query_balance_log(self, request):
        """
        查询余额流水,有流水改动的交易
        :param request:查询条件
        """
        return self.__client.call("eleme.finance.queryBalanceLog", {"request": request})

    def query_head_bills_new(self, shop_id, query):
        """
        查询总店账单(新接口)
        :param shopId:饿了么总店店铺id
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryHeadBillsNew", {"shopId": shop_id, "query": query})

    def query_head_orders_new(self, shop_id, query):
        """
        查询总店订单(新接口)
        :param shopId:饿了么总店店铺id
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryHeadOrdersNew", {"shopId": shop_id, "query": query})

    def query_branch_bills_new(self, shop_id, query):
        """
        查询分店账单(新接口)
        :param shopId:饿了么分店店铺id
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryBranchBillsNew", {"shopId": shop_id, "query": query})

    def query_branch_orders_new(self, shop_id, query):
        """
        查询分店订单(新接口)
        :param shopId:饿了么分店店铺id
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryBranchOrdersNew", {"shopId": shop_id, "query": query})

    def get_order_new(self, shop_id, order_id):
        """
        查询订单(新接口)
        :param shopId:饿了么店铺id
        :param orderId:订单id
        """
        return self.__client.call("eleme.finance.getOrderNew", {"shopId": shop_id, "orderId": order_id})

    def query_allowance_bills(self, shop_id, query):
        """
        查询返现汇总信息账单
        :param shopId:饿了么分店、单店、总店店铺id
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryAllowanceBills", {"shopId": shop_id, "query": query})

    def query_allowance_bill_detail(self, shop_id, query):
        """
        查询返现每日详单
        :param shopId:饿了么分店、单店、总店店铺id
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryAllowanceBillDetail", {"shopId": shop_id, "query": query})

    def query_term_and_name(self, term_and_name_query):
        """
        查询商户帐期和名称
        :param termAndNameQuery:查询条件
        """
        return self.__client.call("eleme.finance.queryTermAndName", {"termAndNameQuery": term_and_name_query})

    def query_by_slave(self, relations_request):
        """
        子资金账号查询关系
        :param relationsRequest:查询条件
        """
        return self.__client.call("eleme.finance.queryBySlave", {"relationsRequest": relations_request})

    def query_slave_shop_ids_by_chain_id(self, chain_id, checkout_date):
        """
        查询连锁总店结算子门店关系列表
        :param chainId:饿了么连锁店店铺id
        :param checkoutDate:入账日期
        """
        return self.__client.call("eleme.finance.querySlaveShopIdsByChainId", {"chainId": chain_id, "checkoutDate": checkout_date})

    def query_goods_orders(self, settle_account_shop_id, shop_id_list, query):
        """
        批量查询分店商品维度的账单数据
        :param settleAccountShopId:结算入账ID
        :param shopIdList:门店id列表（限制100）
        :param query:查询条件
        """
        return self.__client.call("eleme.finance.queryGoodsOrders", {"settleAccountShopId": settle_account_shop_id, "shopIdList": shop_id_list, "query": query})

    def query_head_shop_generic_card_bills(self, page_query):
        """
        分页查询总店通兑卡账单
        :param pageQuery:总店账单分页查询条件
        """
        return self.__client.call("eleme.finance.queryHeadShopGenericCardBills", {"pageQuery": page_query})

    def query_branch_shop_generic_card_bills(self, page_query):
        """
        分页查询分店通兑卡账单列表
        :param pageQuery:分页查询条件
        """
        return self.__client.call("eleme.finance.queryBranchShopGenericCardBills", {"pageQuery": page_query})

    def query_generic_card_bill_by_order(self, order_bill_query):
        """
        查询外卖订单通兑卡账单信息
        :param orderBillQuery:外卖订单查询条件
        """
        return self.__client.call("eleme.finance.queryGenericCardBillByOrder", {"orderBillQuery": order_bill_query})

    def query_chain_shop_reward_bill(self, page_query):
        """
        分页查询店铺返佣账单信息
        :param pageQuery:分页查询返佣账单条件
        """
        return self.__client.call("eleme.finance.queryChainShopRewardBill", {"pageQuery": page_query})

    def query_reward_bill_by_order(self, query):
        """
        查询外卖订单的返佣账单信息
        :param query:分页查询返佣账单条件
        """
        return self.__client.call("eleme.finance.queryRewardBillByOrder", {"query": query})

