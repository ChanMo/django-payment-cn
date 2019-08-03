from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

METHOD_CHOICES = (
    ('wechat', _('wechat')),
    ('alipay', _('alipay'))
)

ACTION_CHOICES = (
    ('recharge', _('recharge')),
    ('shoping', _('shoping'))
)

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
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

    def __str__(self):
        return self.action

    class Meta:
        ordering = ['-created']
        verbose_name = _('log')
        verbose_name_plural = _('log')
