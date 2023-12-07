# -*- coding: utf-8 -*-


# 自然人商户入驻服务
class MerchantService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_merchant_contract_template(self):
        """
        查询商户电子签合同模版
        """
        return self.__client.call("eleme.merchant.getMerchantContractTemplate", {})

    def upload(self, request):
        """
        文件上传(用于资质证照类文件上传)
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.upload", {"request": request})

    def send_verify_code(self, request):
        """
        发送普通短信验证码(下发短信验证码至商户手机号)
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.sendVerifyCode", {"request": request})

    def send_auth_verify_code(self, request):
        """
        实名认证发送验证码请求(此接口用于商户姓名、身份证、手机号或银行卡等关键要素校验, 以及认证验证码的发送)
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.sendAuthVerifyCode", {"request": request})

    def create_apply(self, request):
        """
        创建商户入驻申请
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.createApply", {"request": request})

    def modify_identity_apply(self, request):
        """
        修改商户入驻申请的商户身份信息
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.modifyIdentityApply", {"request": request})

    def modify_auth_apply(self, request):
        """
        修改商户入驻申请的认证信息，需携带实名认证验证码
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.modifyAuthApply", {"request": request})

    def submit_audit(self, request):
        """
        商户入驻申请送审
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.submitAudit", {"request": request})

    def send_sign_verify_code(self, request):
        """
        发送签约短信验证码
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.sendSignVerifyCode", {"request": request})

    def sign_contract(self, request):
        """
        商户签约(签署电子合同)
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.signContract", {"request": request})

    def get_by_id(self, request):
        """
        查询商户入驻申请详情
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.getById", {"request": request})

    def modify_auth_info(self, request):
        """
        修改已生效商户认证信息，需携带实名认证验证码
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.modifyAuthInfo", {"request": request})

    def modify_by_license_type_and_no(self, request):
        """
        根据证件号+证件类型修改商户认证信息，需携带实名认证验证码
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.modifyByLicenseTypeAndNo", {"request": request})

    def get_by_license_type_and_no(self, request):
        """
        根据证件类型+证件号码查询自然人商户(返回信息不包含入驻申请ID和商户ID等信息，且身份信息会脱敏处理)
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.getByLicenseTypeAndNo", {"request": request})

    def get_merchant_by_verify_code(self, request):
        """
        根据证件类型+证件号码查询自然人商户详情，需要携带商户身份签名+短信验证
        :param request:请求参数
        """
        return self.__client.call("eleme.merchant.getMerchantByVerifyCode", {"request": request})

