# -*- coding: utf-8 -*-


# 企业订餐商户服务
class EnterpriseService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def update_ent_arrival_order_relate(self, relate_req_dto):
        """
        关联企业订餐到店订单
        :param relateReqDto:订单关联请求
        """
        return self.__client.call("eleme.enterprise.updateEntArrivalOrderRelate", {"relateReqDto": relate_req_dto})

    def update_ent_arrival_shop_enable(self, enable_request):
        """
        更新企业订餐店铺订单关联启用状态
        :param enableRequest:门店启用请求
        """
        return self.__client.call("eleme.enterprise.updateEntArrivalShopEnable", {"enableRequest": enable_request})

    def update_arrival_shop_online_order_enable(self, enable_request):
        """
        更新企业订餐店铺在线点餐启用状态
        :param enableRequest:门店启用请求
        """
        return self.__client.call("eleme.enterprise.updateArrivalShopOnlineOrderEnable", {"enableRequest": enable_request})

    def get_user_authentication(self, req):
        """
        获取饿了么企餐用户认证
        :param req:饿了么企餐用户
        """
        return self.__client.call("eleme.enterprise.getUserAuthentication", {"req": req})

    def create_online_order(self, create_req):
        """
        ISV创建饿了么订单，获取订单编号
        :param createReq:创单参数
        """
        return self.__client.call("eleme.enterprise.createOnlineOrder", {"createReq": create_req})

    def push_order_detail(self, detail_req):
        """
        ISV订单详情同步
        :param detailReq:订单详情
        """
        return self.__client.call("eleme.enterprise.pushOrderDetail", {"detailReq": detail_req})

    def load_payment_page(self, req):
        """
        加载企业订餐买单页面
        :param req:买单参数
        """
        return self.__client.call("eleme.enterprise.loadPaymentPage", {"req": req})

    def get_ent_arrival_order_detail(self, order_req_dto):
        """
        企业付订单查询接口
        :param orderReqDto:订单请求
        """
        return self.__client.call("eleme.enterprise.getEntArrivalOrderDetail", {"orderReqDto": order_req_dto})

