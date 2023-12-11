# This is a Example file，Creat at 2023/12/10
# python: py3.x[all]
# install this sdk:pip install quanmsms
from quanmsms import sdk

if __name__ == '__main__':
    # openID和Apikey可以在 https://dev.quanmwl.com/ability_sms 查看到
    # 其中，模板可以在测试接口成功后申请自定义模板
    sms = sdk.SDK(
        '2',  # OpenID
        'wd4wa8d4a98w94d89wefwsef4ae9f7ad59ae46s7te49g7t4g9y65h' # Apikey
    )
    #                     手机号      模板id   模板参数
    sendOK, info = sms.send('19954761564', 0, {'code': 12344})
    print(sendOK) # 是否成功(布尔值)
    print(info) # 描述信息 
