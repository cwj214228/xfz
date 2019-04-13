from django import forms
from apps.forms import FormMimin


class LoginForm(forms.Form,FormMimin):
    telephone=forms.CharField(max_length=11,error_messages={"max_length":"账号长度最多不能超过11位"})
    password=forms.CharField(min_length=6,max_length=20,error_messages={"min_length":"密码最短不能少于6位",
                                                                        "max_length":"密码最长不能超过20位"})
    remenber=forms.IntegerField(required=False)

