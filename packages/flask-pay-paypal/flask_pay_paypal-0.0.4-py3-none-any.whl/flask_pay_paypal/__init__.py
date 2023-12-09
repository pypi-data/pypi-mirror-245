"""
 Flask-Pay-PayPal
 # ~~~~~~~~~~~~~~
 flask 短信 扩展
 Flask SMS extension
 :copyright: (c) 2023.11 by 浩.
 :license: GPL, see LICENSE for more details.
"""
import requests
from requests.auth import HTTPBasicAuth

import json
from datetime import datetime


# 限制短信频率


class Paypal(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            print("init_app")
            self.init_app(app)

    def init_app(self, app):
        # 兼容 0.7 以前版本
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        # 在 app 应用中存储所有扩展实例, 可验证扩展是否完成实例化
        app.extensions['sms'] = self

        # 扩展配置， 初始化后添加到 app.config 中, 以 SHARE_ 开头避免冲突
        app.config.setdefault('PAYPAL_client_id',
                              'AUQXv1YCePlbklNVI1rDYu8XAD_TOETzOGhOB8duEeMMRHixfjbK_QmXhxpoXmEwxEu9kh1SKKm0R1lb')
        app.config.setdefault('PAYPAL_client_secret',
                              "ECU_72JexlwAhn6-7hGyh3W6-kYpnf526Iu9zQxtPgEvN0tk3WSjr-zbQjTExhEFy1xFOIKVcY15tdK0")
        app.config.setdefault('PAYPAL_model', 'sandbox')
        app.config.setdefault('PAYPAL_return_url', 'http://127.0.0.1:5000/paypal/return')
        app.config.setdefault('PAYPAL_cancel_url', 'http://127.0.0.1:5000/paypal/cancel')
        self.init()
        self.get_access_token()

    def init(self):
        config = self.app.config.copy()
        print(config)
        self.client_id = config['PAYPAL_client_id']
        self.client_secret = config['PAYPAL_client_secret']
        self.return_url = config['PAYPAL_return_url']
        self.cancel_url = config['PAYPAL_cancel_url']


        if config['PAYPAL_model'] == 'sandbox':
            self.base_url = 'https://api-m.sandbox.paypal.com'
        else:
            self.base_url = 'https://api-m.paypal.com'

    def get_access_token(self):

        token_url = "{base_url}/v1/oauth2/token".format(base_url=self.base_url)
        client_id = self.client_id
        client_secret = self.client_secret

        # 构建请求头
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # 构建请求数据
        data = {
            "grant_type": "client_credentials",
        }

        # 发送 POST 请求获取访问令牌
        response = requests.post(
            token_url,
            auth=HTTPBasicAuth(client_id, client_secret),
            headers=headers,
            data=data
        )

        # 解析响应数据
        token_data = response.json()

        # 提取访问令牌
        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in")

        self.access_token = access_token

        print("Access Token: {access_token}".format(access_token=access_token))
        print("Expires In: {expires_in} seconds".format(expires_in=expires_in))

    def orders_create(self, request_body=None):
        """

        "intent": "CAPTURE",  # 或者 "AUTHORIZE"
        当 `intent` 设置为 "CAPTURE" 时，表示希望立即捕获用户支付的款项。
        这意味着一旦用户支付成功，资金就会被立即从用户账户中扣除。
        `intent` 设置为 "AUTHORIZE" 时，表示希望仅仅授权支付款项，而不立即捕获。

        "USD" 表示美元。
        value: 表示支付的具体金额。

        payment_method_preference: 表示支付方式的偏好设置。在这个例子中，设置为 "IMMEDIATE_PAYMENT_REQUIRED"，表示要求立即支付。
        brand_name: 商户的品牌名称。在这个例子中，设置为 "EXAMPLE INC"。
        locale: 语言环境设置。在这个例子中，设置为 "en-US"，表示英语（美国）。
        landing_page: 登录后的着陆页设置。在这个例子中，设置为 "LOGIN"，表示登录后的着陆页是登录页。
        shipping_preference: 运送偏好设置。在这个例子中，设置为 "SET_PROVIDED_ADDRESS"，表示使用提供的地址进行运送。
        user_action: 用户的操作设置。在这个例子中，设置为 "PAY_NOW"，表示用户点击后立即支付。


        return_url:用于指定用户成功完成支付后将被重定向到的 URL。
        cancel_url: 用于指定用户取消支付后将被重定向到的 URL。

        """

        # PayPal API配置
        api_url = "{base_url}/v2/checkout/orders".format(base_url=self.base_url)
        access_token = self.access_token

        # 构建请求头
        headers = {
            'PayPal-Request-Id': self.get_order_number(),
            "Content-Type": "application/json",
            "Authorization": "Bearer {access_token}".format(access_token=access_token),
        }

        # 构建请求体
        if request_body is None:
            request_body = {
                "intent": "CAPTURE",
                "purchase_units": [{

                    "amount": {
                        "currency_code": "USD",
                        "value": "1.00"}
                }],

                "application_context": {
                    "return_url": self.return_url,
                    "cancel_url": self.cancel_url
                }

            }

        # 发送 POST 请求创建订单
        response = requests.post(api_url, headers=headers, data=json.dumps(request_body))

        # 解析响应数据
        order_data = response.json()

        # 处理返回的数据
        print(order_data)
        return order_data

    def orders_order_example(self):
        d = {
            "intent": "CAPTURE",
            "purchase_units": [{

                "amount": {
                    "currency_code": "USD",
                    "value": "1.00"}
            }],

            "application_context": {
                "return_url": "https://example.com/returnUrl",
                "cancel_url": "https://example.com/cancelUrl"
            }

        }

        return d

    def get_order_number(self):

        now = datetime.now()
        order_number = now.strftime("%Y%m%d%H%M%S%f")  # 格式化日期时间为字符串
        return order_number

    def confirm_the_order(self, order_id, payer_id):
        """
       Confirm the Order 捕获订单付款
       :return:
       """
        headers = {
            'Authorization': 'Bearer {access_token}'.format(access_token=self.access_token),
        }

        # PayPal 订单确认和执行支付的端点
        capture_endpoint = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/{id}/capture'.format(id=order_id)

        # 构建请求体
        request_body = {
            'payer_id': payer_id,
        }

        # 发送 POST 请求确认和执行支付
        response = requests.post(capture_endpoint, headers=headers, json=request_body)

        # 解析响应数据
        capture_data = response.json()

        # 处理支付结果
        if response.status_code == 201:
            print('Payment captured successfully!')
            # 在这里可以进行支付成功后的其他处理
            return response.json()
        else:
            print('Error capturing payment: {json.dumps(capture_data, indent=2)}')
            # 在这里可以处理支付失败的情况
            return response.json()
