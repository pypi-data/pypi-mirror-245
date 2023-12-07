# -*- coding: utf-8 -*-


# 商家服务中台服务
class MsorderService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_list(self, query_list_request):
        """
        服务单-列表查询
        :param queryListRequest:服务单列表查询入参
        """
        return self.__client.call("eleme.msorder.queryList", {"queryListRequest": query_list_request})

    def query_complaint_detail(self, query_complaint_detail_request):
        """
        投诉单-明细查询
        :param queryComplaintDetailRequest:投诉单详情入参
        """
        return self.__client.call("eleme.msorder.queryComplaintDetail", {"queryComplaintDetailRequest": query_complaint_detail_request})

    def complaint_agree(self, complaint_agree_request):
        """
        投诉单-协商同意
        :param complaintAgreeRequest:商户同意投诉入参
        """
        return self.__client.call("eleme.msorder.complaintAgree", {"complaintAgreeRequest": complaint_agree_request})

    def complaint_apply_platform(self, complaint_apply_platform_request):
        """
        投诉单-申请平台介入
        :param complaintApplyPlatformRequest:商家申请平台介入入参
        """
        return self.__client.call("eleme.msorder.complaintApplyPlatform", {"complaintApplyPlatformRequest": complaint_apply_platform_request})

    def complaint_send_voucher(self, complaint_send_voucher_request):
        """
        投诉单-发券
        :param complaintSendVoucherRequest:商家发券入参
        """
        return self.__client.call("eleme.msorder.complaintSendVoucher", {"complaintSendVoucherRequest": complaint_send_voucher_request})

