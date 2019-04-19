from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse
from utils import restful
from django.shortcuts import redirect,reverse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from utils.aliyunsdk import aliyunsms
from django.core.cache import cache
from django.contrib.auth import get_user_model

User=get_user_model()


# Create your views here.
@require_POST
def login_views(request):
    # 获取用户post上来的表单
    form=LoginForm(request.POST)
    # 对表单进行验证，就是把客户端提交上来的数据和自己定义的form进行验证
    if form.is_valid():
        print('表单检验成功')
        telephone=form.cleaned_data.get('telephone')
        password=form.cleaned_data.get('password')
        remember=form.cleaned_data.get('remember')
        # 对账号和密码进行认证

        user=authenticate(request,username=telephone,password=password)
        print(str(user)+'认证成功')
        if user:
            if user.is_active:
                print(str(user) + '用户没有被封')
                # 用户登陆
                login(request,user)
                if remember:
                    # None表示默认，默认是2周
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="您的账号已经被冻结")
        else:
            return restful.params_error(message="手机号或者密码错误")
    else:
        errors=form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def img_captcha(request):
    # 获取验证码的图片和文字
    text,image=Captcha.gene_code()
    out=BytesIO()
    image.save(out,'png')
    out.seek(0)
    # 返回的类型是图片
    response=HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length']=out.tell()
    # 以验证码的小写为key，验证码的小写为value，保存再服务器的缓存中2分钟
    cache.set(text.lower(), text.lower(), 2*60)
    return response


def sms_captcha(request):
    # 通过GET获取用户提交上来的telephone
    telephone=request.GET.get('telephone')
    # 随机生成一个4为的验证码
    code = Captcha.gene_text()
    # 以telephone为key，以code为value，把手机验证码缓存在服务器的内存中
    cache.set(telephone, code, 2 * 60)
    # 通过阿里云短信服务给用户发送验证短信
    result=aliyunsms.send_Sms(telephone,code)
    print(result)
    print(code)
    return restful.ok()

@require_POST
def register(request):
    # 获取用户提交的表单，交给RegisterForm
    form=RegisterForm(request.POST)
    # 表单验证
    if form.is_valid():
        print('表单检验成功')
        username=form.cleaned_data.get('username')
        telephone=form.cleaned_data.get('telephone')
        password=form.cleaned_data.get('password1')
        # 用户注册，数据保存到数据库中
        user=User.objects.create_user(telephone=telephone,username=username,password=password)
        print(user+'用户注册成功')
        # 用户登陆
        login(request,user)
        print(user+'用户登陆成功')
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())

