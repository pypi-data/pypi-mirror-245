# -*- coding: utf-8 -*-


# 开放平台用户信息查询服务
class AucService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_user_pre_auth_token(self, request):
        """
        获取预授权令牌
        :param request:查询条件
        """
        return self.__client.call("eleme.auc.getUserPreAuthToken", {"request": request})

    def query_user_info_by_token(self, request):
        """
        根据令牌查询用户信息
        :param request:查询条件
        """
        return self.__client.call("eleme.auc.queryUserInfoByToken", {"request": request})

