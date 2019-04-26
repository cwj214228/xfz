from django import forms
from apps.forms import FormMimin

class PublicCommentForm(forms.Form, FormMimin):
    content = forms.CharField()
    news_id = forms.IntegerField()

