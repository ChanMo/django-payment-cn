import decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.test import APITestCase
from wallet.models import Wallet

from .models import Log

User = get_user_model()


# class AlipayNotifyTest(TestCase):
#     number = '000000001'
#     def setUp(self):
#         self.user = user = User.objects.create_user('test')
#         Log.objects.create(
#             method = 'alipay',
#             user = user,
#             action = 'recharge',
#             number = self.number,
#             amount = 0.1,
#             description = 'test',
#             extra = 'test',
#         )
#
#     def test(self):
#         c = Client()
#         data = {
#                 'total_amount': 0.1,
#                 'out_trade_no': '000000001',
#                 'trade_status': 'TRADE_SUCCESS'
#                 }
#         res = c.post('/payment/notify/alipay/', data)
#         self.assertEqual(res.content.decode('utf8'), "success")
#         self.assertTrue(Log.objects.get(number=self.number).is_success)
#         self.assertEqual(float(Wallet.objects.get(user=self.user).amount), 0.1)
#
#
# class AlipayTest(APITestCase):
#     def setUp(self):
#         user = User.objects.create_user('test')
#         self.client.force_authenticate(user=user)
#
#     def test(self):
#         data = {
#                 'amount': 100,
#                 'platform': 'alipay'
#                 }
#         res = self.client.post('/payment/pay/', data)
#         print(res.data)
#         self.assertEqual(res.status_code, 200)
#
#
# class PayTest(APITestCase):
#     def setUp(self):
#         user = User.objects.create_user('test')
#         self.client.force_authenticate(user=user)
#
#     def test(self):
#         data = {
#             'amount': 100
#         }
#         res = self.client.post('/payment/pay/', data)
#         print(res.data)
#         self.assertEqual(res.status_code, 200)
#
#
# class Notify(APITestCase):
#     def setUp(self):
#         self.user = user = User.objects.create_user('test')
#         Log.objects.create(
#             method = 'wechat',
#             user = user,
#             action = 'recharge',
#             number = '1409811653',
#             amount = 0.1,
#             description = 'test',
#             extra = 'test',
#         )
#
#     def test(self):
#         data = """<xml>
#   <appid><![CDATA[wx2421b1c4370ec43b]]></appid>
#   <attach><![CDATA[支付测试]]></attach>
#   <bank_type><![CDATA[CFT]]></bank_type>
#   <fee_type><![CDATA[CNY]]></fee_type>
#   <is_subscribe><![CDATA[Y]]></is_subscribe>
#   <mch_id><![CDATA[10000100]]></mch_id>
#   <nonce_str><![CDATA[5d2b6c2a8db53831f7eda20af46e531c]]></nonce_str>
#   <openid><![CDATA[oUpF8uMEb4qRXf22hE3X68TekukE]]></openid>
#   <out_trade_no><![CDATA[1409811653]]></out_trade_no>
#   <result_code><![CDATA[SUCCESS]]></result_code>
#   <return_code><![CDATA[SUCCESS]]></return_code>
#   <sign><![CDATA[B552ED6B279343CB493C5DD0D78AB241]]></sign>
#   <sub_mch_id><![CDATA[10000100]]></sub_mch_id>
#   <time_end><![CDATA[20140903131540]]></time_end>
#   <total_fee>1</total_fee><coupon_fee><![CDATA[10]]></coupon_fee>
# <coupon_count><![CDATA[1]]></coupon_count>
# <coupon_type><![CDATA[CASH]]></coupon_type>
# <coupon_id><![CDATA[10000]]></coupon_id>
# <coupon_fee_0><![CDATA[100]]></coupon_fee_0>
#   <trade_type><![CDATA[JSAPI]]></trade_type>
#   <transaction_id><![CDATA[1004400740201409030005092168]]></transaction_id>
# </xml>"""
#         c = Client()
#         res = c.post('/payment/notify/wechat/', data, 'text/plain')
#         print(res.content)
#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(Log.objects.get(number='1409811653').is_success)
#         self.assertEqual(float(Wallet.objects.get(user=self.user).amount), 0.1)
