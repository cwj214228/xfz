from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def send_Sms(PhoneNumbers,code):
    client = AcsClient('LTAI1yzeitQRYJLk', 'sTWMKFFx0H63ilb3YIYMlkpirE9Mhu', 'cn-hangzhou')
    TemplateParam={"code":code}
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PhoneNumbers',PhoneNumbers)
    request.add_query_param('SignName', '小饭桌')
    request.add_query_param('TemplateCode', 'SMS_163432566')
    request.add_query_param('TemplateParam', TemplateParam)#TemplateParam: '{"code":"1111"}'

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    return str(response, encoding='utf-8')