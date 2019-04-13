from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse
from utils import restful

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