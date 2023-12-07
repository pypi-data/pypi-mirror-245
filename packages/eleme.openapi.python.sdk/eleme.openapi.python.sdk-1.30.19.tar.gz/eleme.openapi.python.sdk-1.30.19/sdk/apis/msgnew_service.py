# -*- coding: utf-8 -*-


# 新消息服务
class MsgnewService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_push_fail_msg(self, msg_query_request):
        """
        获取推送失败的消息列表
        :param msgQueryRequest:查询条件
        """
        return self.__client.call("eleme.msgNew.getPushFailMsg", {"msgQueryRequest": msg_query_request})

    def confirm_pull_msg(self, msg_confirm_request):
        """
        向平台确认已成功拉取推送失败的消息
        :param msgConfirmRequest:查询条件
        """
        return self.__client.call("eleme.msgNew.confirmPullMsg", {"msgConfirmRequest": msg_confirm_request})

