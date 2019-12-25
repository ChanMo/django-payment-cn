import logging
import random

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from wechat.base import Wechat
from wechat.wxa import Wxa

logger = logging.getLogger(__name__)

METHOD_CHOICES = (
    ('douyin', _('douyin')),
    ('wechat', _('wechat')),
    ('alipay', _('alipay'))
)

ACTION_CHOICES = (
    ('recharge', _('recharge')),
    ('shopping', _('shopping'))
)

class LogManager(models.Manager):
    def get_wxa_data(self, request, amount, number, desc, action, extra=None):
        """
        获取小程序客户端支付数据

        amount: 金额, 单位元
        number: 基础编号
        desc: 支付单描述
        action: 事件类型(recharge, shopping)
        extra: 其他数据
        """
        wxa = Wxa()
        number = '{}{}'.format(number, random.randint(1000,9999)) # 随机数
        data = {
          'body': desc,
          'out_trade_no': number,
          'total_fee': int(amount*100),
          'spbill_create_ip': request.META['REMOTE_ADDR'],
          'notify_url': 'https://{}/payment/notify/wechat/'.format(request.site),
          'trade_type': 'JSAPI', # 小程序
          'openid': request.user.get_wxa_openid() # JSAPI时必传
          }
        prepayid = wxa.get_prepay_id(data)
        data = wxa.get_pay_data(prepayid)

        self.create(user=request.user,
                method='wechat',
                action=action,
                number=number,
                amount=amount,
                description=desc,
                extra=extra)

        return data


class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='pay_log', verbose_name=_('user'))
    method = models.CharField(_('method'), max_length=50, default='wechat',
            choices=METHOD_CHOICES)
    action = models.CharField(_('action'), max_length=50,
            default='recharge', choices=ACTION_CHOICES)
    openid = models.CharField(_('openid'), max_length=50, blank=True,
            null=True)
    number = models.CharField(_('number'), max_length=50, unique=True)
    amount = models.DecimalField(_('amount'), max_digits=12,
            decimal_places=2)
    description = models.TextField(_('description'), blank=True, null=True)
    extra = models.TextField(_('extra'), blank=True, null=True)
    is_success = models.BooleanField(_('is success'), default=False)
    error_msg = models.CharField(_('error message'), max_length=255,
            blank=True, null=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    objects = LogManager()

    def __str__(self):
        return self.action

    class Meta:
        ordering = ['-created']
        verbose_name = _('payment log')
        verbose_name_plural = _('payment log')
