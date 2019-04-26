from apps.forms import FormMimin
from django import forms
from apps.news.models import News
from apps.course.models import Course


class EditNewsCategoryForm(forms.Form):
    pk = forms.IntegerField()
    name = forms.CharField(max_length=100)


class EditNewsForm(forms.ModelForm, FormMimin):
    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class WriteNewsForm(forms.ModelForm, FormMimin):
    category = forms.IntegerField()

    # pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class PubCourseForm(forms.ModelForm, FormMimin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ("category", 'teacher')
