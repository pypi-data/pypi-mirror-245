# -*- coding: utf-8 -*-


# 视频服务
class ContentService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def upload_video(self, o_video_info, shop_id, video_type):
        """
        上传视频
        :param oVideoInfo:视频信息
        :param shopId:店铺Id
        :param videoType:视频类型
        """
        return self.__client.call("eleme.content.uploadVideo", {"oVideoInfo": o_video_info, "shopId": shop_id, "videoType": video_type})

    def get_efs_config(self, video_type):
        """
        获取efs配置
        :param videoType:视频类型
        """
        return self.__client.call("eleme.content.getEfsConfig", {"videoType": video_type})

    def set_video_bind_relation(self, video_id, biz_id, bind_biz_type):
        """
        建立视频与相对应的业务的关联关系
        :param videoId:视频Id
        :param bizId:业务Id(如业务类型为GOOD，业务Id为商品Id)
        :param bindBizType:业务类型
        """
        return self.__client.call("eleme.content.setVideoBindRelation", {"videoId": video_id, "bizId": biz_id, "bindBizType": bind_biz_type})

    def unset_video_bind_relation(self, video_id, biz_id, bind_biz_type):
        """
        取消视频与对应业务的关联关系
        :param videoId:视频Id
        :param bizId:业务Id(如业务类型为GOOD，业务Id为商品Id)
        :param bindBizType:业务类型
        """
        return self.__client.call("eleme.content.unsetVideoBindRelation", {"videoId": video_id, "bizId": biz_id, "bindBizType": bind_biz_type})

    def get_video_info(self, video_id):
        """
        通过视频id查询视频信息
        :param videoId:视频Id
        """
        return self.__client.call("eleme.content.getVideoInfo", {"videoId": video_id})

    def get_video_bind_info(self, video_id):
        """
        通过视频id获取所有相关联的业务关系
        :param videoId:视频Id
        """
        return self.__client.call("eleme.content.getVideoBindInfo", {"videoId": video_id})

    def get_upload_token(self, scene):
        """
        获取视频上传token
        :param scene:场景码
        """
        return self.__client.call("eleme.content.getUploadToken", {"scene": scene})

    def publish_video_content(self, request):
        """
        发布视频
        :param request:内容发布对象
        """
        return self.__client.call("eleme.content.publishVideoContent", {"request": request})

