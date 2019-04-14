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
    form=LoginForm(request.POST)
    if form.is_valid():
        telephone=form.cleaned_data.get('telephone')
        password=form.cleaned_data.get('password')
        remenber=form.cleaned_data.get('remenber')
        user=authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remenber:
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
    text,image=Captcha.gene_code()
    out=BytesIO()
    image.save(out,'png')
    out.seek(0)
    response=HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length']=out.tell()
    cache.set(text.lower(), text.lower(), 2*60)
    return response


def sms_captcha(request):
    telephone=request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone, code, 2 * 60)
    # result=aliyunsms.send_Sms(telephone,code)
    # print(result)
    print(code)
    return restful.ok()

@require_POST
def register(request):
    form=RegisterForm(request.POST)
    print(form.is_valid())

    if form.is_valid():
        username=form.cleaned_data.get('username')
        telephone=form.cleaned_data.get('telephone')
        password=form.cleaned_data.get('password1')
        user=User.objects.create_user(telephone=telephone,username=username,password=password)

        login(request,user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())

