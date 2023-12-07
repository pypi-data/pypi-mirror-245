# -*- coding: utf-8 -*-


# 开店服务
class OpenshopService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_all_catering_category(self):
        """
        获取所有餐饮频道的类目信息
        """
        return self.__client.call("eleme.openShop.getAllCateringCategory", {})

    def get_all_division_info(self):
        """
        获取所有行政区划信息
        """
        return self.__client.call("eleme.openShop.getAllDivisionInfo", {})

    def upload_file(self, request):
        """
        资质证照类文件上传
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.uploadFile", {"request": request})

    def save_draft(self, request):
        """
        保存草稿
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.saveDraft", {"request": request})

    def get_draft(self, request):
        """
        查询草稿
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.getDraft", {"request": request})

    def pre_check(self, request):
        """
        开店申请预校验
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.preCheck", {"request": request})

    def submit(self, request):
        """
        提交开店申请
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.submit", {"request": request})

    def get_detail_by_apply_id(self, request):
        """
        查询开店申请
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.getDetailByApplyId", {"request": request})

    def create(self, request):
        """
        创建开店申请
        :param request:请求参数
        """
        return self.__client.call("eleme.openShop.create", {"request": request})

