import hashlib
import json
import logging
import random
import string
import time
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

class Douyin:
    """
    抖音支付
    """
    def __init__(self):
        self.appid = settings.DOUYIN['appid']
        self.mch_id = settings.DOUYIN['mch_id']
        self.key = settings.DOUYIN['key']

    def _make_sign(self, data):
        "生成签名"
        data = urllib.parse.urlencode(sorted(data.items()))
        data = urllib.parse.unquote(data)
        data += self.key
        data = str.encode(data)
        data = hashlib.md5(data).hexdigest()
        logger.warning(data)

        return data

    def _make_nonce(self, length=32):
        "生成随即字符串"

        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def get_pay_data(self, order, ip, alipay):
        " 获取支付数据 "
        data = {
            'merchant_id': self.mch_id,
            'app_id': self.appid,
            'sign_type': 'MD5',
            'timestamp': str(int(time.time())),
            'product_code': 'pay',
            'payment_type': 'direct',
            'out_order_no': order.number,
            'uid': str(order.user.id),
            'version': '2.0',
            'total_amount': int(order.amount*100),
            'currency':  'CNY',
            'subject': order.description,
            'body': order.description,
            'trade_time': str(int(time.time())),
            'valid_time': str(60*30),
            'notify_url': '',
            'alipay_url': alipay,
        }
        data['sign'] = self._make_sign(data)

        return data



    # def get_pay_data2(self, order, ip, alipay):
    #     " 获取支付数据requestpayment方式 "
    #     uid = order.user.social_set.filter(provider__name='douyin')[0].uid
    #     data = {
    #         'app_id': self.appid,
    #         'method': 'tp.trade.confirm',
    #         'sign_type': 'MD5',
    #         'timestamp': str(int(time.time())),
    #         'trade_no': order.number,
    #         'merchant_id': self.mch_id,
    #         'uid': uid,
    #         'total_amount': int(order.amount*100),
    #         'pay_channel': 'ALIPAY_NO_SIGN',
    #         'pay_type': 'ALIPAY_APP',
    #         'params': json.dumps({
    #             'url': alipay
    #             }),
    #         'risk_info': json.dumps({
    #             'ip': ip
    #             })
    #     }
    #     data['sign'] = self._make_sign(data)

    #     return data
