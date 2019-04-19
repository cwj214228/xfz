
from apps.forms import FormMimin
from django import forms
from apps.news.models import News


class EditNewsCategoryForm(forms.Form):
    pk = forms.IntegerField()
    name = forms.CharField(max_length=100)


class EditNewsForm(forms.ModelForm,FormMimin):
    category = forms.IntegerField()
    pk = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['category','author','pub_time']


class WriteNewsForm(forms.ModelForm,FormMimin):
    category = forms.IntegerField()
    # pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']
