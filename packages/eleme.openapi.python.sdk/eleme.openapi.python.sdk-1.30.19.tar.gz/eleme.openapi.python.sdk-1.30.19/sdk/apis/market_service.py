# -*- coding: utf-8 -*-


# 服务市场服务
class MarketService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def sync_market_messages(self, start, end, offset, limit):
        """
        同步某一段时间内的服务市场消息
        :param start:开始时间
        :param end:结束时间
        :param offset:消息偏移量
        :param limit:查询消息数
        """
        return self.__client.call("eleme.market.syncMarketMessages", {"start": start, "end": end, "offset": offset, "limit": limit})

    def create_order(self, request):
        """
        创建内购项目订单
        :param request:创建订单请求信息
        """
        return self.__client.call("eleme.market.createOrder", {"request": request})

    def query_order(self, order_no):
        """
        查询服务市场订单
        :param orderNo:服务市场订单编号
        """
        return self.__client.call("eleme.market.queryOrder", {"orderNo": order_no})

    def confirm_order(self, order_no):
        """
        服务市场确认订单
        :param orderNo:服务市场订单编号
        """
        return self.__client.call("eleme.market.confirmOrder", {"orderNo": order_no})

    def mark_finish_cooking_time(self, device_info, order_id):
        """
        物联网设备确认出餐
        :param deviceInfo:设备信息
        :param orderId:订单id
        """
        return self.__client.call("eleme.market.markFinishCookingTime", {"deviceInfo": device_info, "orderId": order_id})

    def upload_logistic_info(self, logistic_infos):
        """
        线下服务上传订单物流单号
        :param logisticInfos:订单物流信息(最多100条)
        """
        return self.__client.call("eleme.market.uploadLogisticInfo", {"logisticInfos": logistic_infos})

    def get_upload_file_signature_info(self):
        """
        获取文件上传秘钥信息
        """
        return self.__client.call("eleme.market.getUploadFileSignatureInfo", {})

    def upload_image_info(self, image_infos):
        """
        上传图片信息
        :param imageInfos:图片信息(最多100条)
        """
        return self.__client.call("eleme.market.uploadImageInfo", {"imageInfos": image_infos})

    def query_offline_order(self, order_no):
        """
        查询服务市场线下服务订单
        :param orderNo:服务市场订单编号
        """
        return self.__client.call("eleme.market.queryOfflineOrder", {"orderNo": order_no})

