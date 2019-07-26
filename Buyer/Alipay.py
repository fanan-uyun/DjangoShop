from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv66JqpsopyoXYMiWiIgyV4O/nc4ptXjRgZO9dkKRzsh1LusdILASoXlZ65nx/4ONCDpFn5QEQQNerVtmCW+Y9N/GmNnQOsEeX5tCxfNlg7vHS5Hk8QDCgIbEzVC3K+9wwYiCc8aQRjSM+Czb/Tq3kI+XJpDIGE6lPtp2zkwZaPt3y8yt88MpYcqPllNn3acEW8U5LnQmMHosohqlXu5iPK57OC7a0oC5AwUPlZcMizO2EqmxonWpfqk+scOhVdyVUwuX6siye76OkUuhO8M1758hhhNOUhmzhurEEW20toqA2eoMP63GweyTt5kWmWcqc30YU0FAN8Aq3QG03wF3xQIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAv66JqpsopyoXYMiWiIgyV4O/nc4ptXjRgZO9dkKRzsh1LusdILASoXlZ65nx/4ONCDpFn5QEQQNerVtmCW+Y9N/GmNnQOsEeX5tCxfNlg7vHS5Hk8QDCgIbEzVC3K+9wwYiCc8aQRjSM+Czb/Tq3kI+XJpDIGE6lPtp2zkwZaPt3y8yt88MpYcqPllNn3acEW8U5LnQmMHosohqlXu5iPK57OC7a0oC5AwUPlZcMizO2EqmxonWpfqk+scOhVdyVUwuX6siye76OkUuhO8M1758hhhNOUhmzhurEEW20toqA2eoMP63GweyTt5kWmWcqc30YU0FAN8Aq3QG03wF3xQIDAQABAoIBAHSkuL+qJcX79jf+OKSjBMd+s/dKwtTczdklV5EEl4gXMkA38QS4QM4kc5TMnJgZrJQKKd4fC6uoak/iI6iwUYsKNedD/NQUOvCBIdQl9muAtJmHEaObC8F8wXwTlzPURHBxKrlbZuZiCjrnyYNC3PvKdXeReUJZcXNbLBsD8h6QgVOPaKXnLCSTZf98gHXkDN0IWlNp08143b4Xp6DO+CiaUHUbUrAcHdB+gHQJnN3+YP3dnVGzvyRisjJ8B8mTS1zPk4fpciViA6EMCYLHFCrS+8LZ+WEpJN8o/0o9Mgpd8YPKg1q4WDlYp1ulnRUVqOkJaVZVOvecTtbPbyaJWUECgYEA9fj7peww3VmPNYS3WAAtm/M5YMgsuFNRWC61/o+FKDSVlH57dVRRTnnGF7NE5dUHldloAa+yBw5Zbi/s5LjYV36zvga4dYZpA8Lt4uglzg3QAXwQ+X5YRqkde1gGolOdU/MsnhvehQpdOoZ5XWzJHe/2kA8RNraZyYsER0PQ2hECgYEAx373L2VZZdhPT8EIrgrAU93izxZAS9Cp5A/whogxmVhaKfGHcJa4YygajzyKd3DRoSmYtbXqysGXZyY+RmolCyMeZEBZ1s/2DTj2vtdh3ngV6UQY4vbgpCBgDCOnoiAq/5whcFcTDjma79BmsdHng/ZXgo+5U6v4TrKdZ7ay7nUCgYEArEZnkk175/xLFjPO6d6uExTmMgfhcnRAe9+zbgh9PayeuzNfKs0UaT9W49CWR9bNikGL2+p/aPu+3TLJ22QvehBuuYAhf4bVVGIZlRv9JnV8Ix4PEX9ROqRF1tbPRrADeAHQVSi10D5zD4ORy0JfFg20hi9XYhfAXG12YKd5xtECgYB8t3A6ziZsWCWFG42cmJYSGDYx9pwtiX6cWCarRDuVvTlo3Vkp1t/hBXJNN7Ds6Lf1A/c3KkplhU9sqejmxnbwFn1qeRxxAcO2EnWXazkBBpvUH8FbKrHXiXHiROwInAmlkOsKuzTrgLHO2L9KzYnp4rhkpAtdNrZeJKXo77u+/QKBgF4DmigjHYR32dmKXZQYp2DkM7lFxnuL6McR0r/5b/wkMUPSInCK4n4e8vBH611dkaNNhNSTR5aVsrMZuBGzQrFOGnXawa+PxpGPaVwR/jf/tPCLmsq2KPenQPF15tc+4dosMp726+f+4Klg71qMK8yjGN+fkrHo3Er1y+35Letj
-----END RSA PRIVATE KEY-----"""

# v3.2 实例化支付应用
alipay = AliPay(
    appid = "2016101000652510",
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type= "RSA2"
)

# v3.2 发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="33456", #订单号
    total_amount=str(1000.01),#支付金额
    subject="生鲜交易", #交易主题
    return_url=None,
    notify_url=None
)

print("https://openapi.alipaydev.com/gateway.do?"+order_string)