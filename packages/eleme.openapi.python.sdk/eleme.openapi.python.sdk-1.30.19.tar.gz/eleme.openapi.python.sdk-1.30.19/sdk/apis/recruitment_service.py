# -*- coding: utf-8 -*-


# 招聘市场服务
class RecruitmentService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def upload_resume(self, resume):
        """
        简历回传
        :param resume:简历信息
        """
        return self.__client.call("eleme.recruitment.uploadResume", {"resume": resume})

    def update_job_position_status(self, position_id, status):
        """
        职位状态变更
        :param positionId:职位id
        :param status:变更状态
        """
        return self.__client.call("eleme.recruitment.updateJobPositionStatus", {"positionId": position_id, "status": status})

    def update_resume_status(self, resume_id, status):
        """
        简历状态变更
        :param resumeId:简历id
        :param status:变更状态
        """
        return self.__client.call("eleme.recruitment.updateResumeStatus", {"resumeId": resume_id, "status": status})

    def update_position_expose_data(self, position_id, expose_count, visit_count, data_date):
        """
        回传职位曝光数据
        :param positionId:职位id
        :param exposeCount:曝光数量
        :param visitCount:访问数量
        :param dataDate:数据日期
        """
        return self.__client.call("eleme.recruitment.updatePositionExposeData", {"positionId": position_id, "exposeCount": expose_count, "visitCount": visit_count, "dataDate": data_date})

    def get_shop_job_infos(self):
        """
        获取商户目前在架以及审核中岗位
        """
        return self.__client.call("eleme.recruitment.getShopJobInfos", {})

