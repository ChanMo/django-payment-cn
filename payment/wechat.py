import hashlib
import logging
import random
import string
import time
import urllib.parse
import urllib.request

import dicttoxml
import xmltodict
from django.conf import settings

logger = logging.getLogger(__name__)

class Wechat:
    """
    微信支付
    """
    def __init__(self):
        self.appid = settings.WECHAT['appid']
        self.mch_id = settings.WECHAT['mch_id']
        self.key = settings.WECHAT['key']

    def _make_sign(self, data):
        "生成微信签名"
        data = urllib.parse.urlencode(sorted(data.items()))
        data = urllib.parse.unquote(data)
        data += '&key=' + self.key
        data = str.encode(data)

        return hashlib.md5(data).hexdigest().upper()

    def _make_nonce(self, length=32):
        "生成随即字符串"

        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def get_pay_data(self, order, ip):
        " 获取支付数据 "
        success, prepay_id = self._get_prepay_id(order, ip)

        if not success:
            return {'detail':prepay_id}
        data = {
            'appid': self.appid,
            'partnerid': self.mch_id,
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': self._make_nonce(),
            'timestamp': str(int(time.time()))
        }
        data['sign'] = self._make_sign(data)

        return data

    def _get_prepay_id(self, order, ip):
        "获取prepayID"
        data = {
            'xml': {
            'appid': self.appid,
            'mch_id': self.mch_id,
            'nonce_str': self._make_nonce(),
            'body': order.get_action_display(),
            'out_trade_no': order.number,
            'total_fee': int(order.amount*100),
            'spbill_create_ip': ip,
            'notify_url': '/payment/notify/wechat/',
            'trade_type': 'APP'
            }
        }
        data['xml']['sign'] = self._make_sign(data['xml'])
        xmldata = dicttoxml.dicttoxml(data, root=False, attr_type=False)
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        req = urllib.request.Request(url=url, data=xmldata)
        with urllib.request.urlopen(req) as f:
            result = f.read().decode('utf8')
            result = xmltodict.parse(result)

            if result['xml']['return_code'] == 'SUCCESS':
                return True, result['xml']['prepay_id']

        return False, result['xml']['return_msg']



    def parse_result(self, result):
        " 解析异步通知返回值 "
        try:
            xmldata = xmltodict.parse(result)

            if xmldata['xml']['return_code'] == 'SUCCESS':
                is_success = True
            else:
                is_success = False

            return True, xmldata['xml']
        except Exception as e:
            logger.debug(e)

            return False, None



    def check_result(self, data):
        " 验证返回值 "

        return True

    def return_failure(self):
        return "<xml><return_code><![CDATA[ERROR]]></return_code><return_msg><![CDATA[ERROR]]></return_msg></xml>"

    def return_success(self):
        return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
