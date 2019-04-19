from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategory,News
from utils import restful
from .forms import EditNewsCategoryForm,WriteNewsForm, EditNewsForm
import os
from django.conf import settings
import qiniu

# Create your views here.

def index(request):
    return render(request, 'cms/index.html')


class WriteNewsView(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_news.html',context=context)
    def post(self,request):
        form=WriteNewsForm(request.POST)

        if form.is_valid():
            title=form.cleaned_data.get('title')
            desc=form.cleaned_data.get('desc')
            thumbnail=form.cleaned_data.get('thumbnail')
            content=form.cleaned_data.get('content')
            category_id=form.cleaned_data.get('category')
            category=NewsCategory.objects.get(pk=category_id)
            print(str(title))
            print(str(desc))
            print(str(thumbnail))
            print(str(content))
            print(str(category_id))
            print(str(category))

            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category,author=request.user)
            return restful.ok()
        else:
            print(str(form.get_errors()))
            return restful.params_error(message=form.get_errors())


class EditNewsView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get("pk")
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context={
        'categories':categories
    }
    return render(request,'cms/news_category.html',context=context)


@require_POST
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')


@require_POST
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该新闻分类不存在')
    else:
        return restful.params_error(message=form.get_error())


@require_POST
def delete_news_category(request):
    pk=request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在')

@require_POST
def upload_file(request):
    file=request.FILES.get('file')
    name=file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url=request.build_absolute_uri(settings.MEDIA_URL+name)
    print(str(url))
    return restful.result(data={'url':url})


@require_GET
def qntoken(request):
    access_key= settings.QINIU_ACCESS_KEY
    secret_key= settings.QINIU_SECRET_KEY
    bucket= settings.QINIU_BUCKET_NAME

    q=qiniu.Auth(access_key,secret_key)
    token=q.upload_token(bucket)
    return restful.result(data={'token':token})