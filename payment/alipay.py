import logging

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import \
    AlipayTradeAppPayRequest
from django.conf import settings

logger = logging.getLogger(__name__)


class Alipay:
    """
    支付宝支付
    """

    def __init__(self):
        self._set_config()
        self.client = DefaultAlipayClient(
                alipay_client_config=self.config,
                logger=logger)

    def _set_config(self):
        " 设置配置项 "
        config = AlipayClientConfig()
        config.server_url = 'https://openapi.alipay.com/gateway.do'
        config.app_id = settings.ALIPAY['appid']
        config.app_private_key = settings.ALIPAY['app_private_key']
        config.alipay_public_key = settings.ALIPAY['alipay_public_key']
        config.sign_type = 'RSA2'
        self.config = config

    def get_pay_data(self, order, ip):
        " 获取支付数据 "
        model = AlipayTradeAppPayModel()
        model.total_amount = str(order.amount)
        model.subject = ""
        model.out_trade_no = order.number
        request = AlipayTradeAppPayRequest(biz_model=model)
        request.notify_url = ''
        response = self.client.sdk_execute(request)

        return {'detail':response}


    def parse_result(self, result):
        " 解析异步通知返回值 "
        try:
            if result['trade_status'] == 'TRADE_SUCCESS':
                is_success = True
            else:
                is_success = False

            return is_success, result
        except KeyError:
            logger.warning('keyerror')

            return False, None



    def check_result(self, data):
        " 验证返回值 "

        return True

    def return_failure(self):
        return "success"

    def return_success(self):
        return "success"
