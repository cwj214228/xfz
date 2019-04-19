from django import forms
from apps.forms import FormMimin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form,FormMimin):
    telephone=forms.CharField(max_length=11,error_messages={"max_length":"账号长度最多不能超过11位"})
    password=forms.CharField(min_length=6,max_length=20,error_messages={"min_length":"密码最短不能少于6位",
                                                                        "max_length":"密码最长不能超过20位"})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMimin):
    telephone = forms.CharField(max_length=11, error_messages={"max_length": "账号长度最多不能超过11位"})
    username=forms.CharField(max_length=20)
    password1 = forms.CharField(min_length=6, max_length=20, error_messages={"min_length": "密码最短不能少于6位",
                                                                            "max_length": "密码最长不能超过20位"})
    password2 = forms.CharField(min_length=6, max_length=20, error_messages={"min_length": "密码最短不能少于6位",
                                                                            "max_length": "密码最长不能超过20位"})
    img_captcha = forms.CharField(min_length=4, max_length=4)
    sms_captcha=forms.CharField(min_length=4, max_length=4)

    def clean(self):
        cleaned_data=super(RegisterForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha=cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower()!=img_captcha.lower():
            raise forms.ValidationError('图形验证码错误')
        telephone=cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha=cache.get(telephone)
        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误')

        exists=User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('该手机号码已经被注册 ')



