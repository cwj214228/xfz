from django.shortcuts import render
from .models import NewsCategory, News, Comment
from django.conf import settings
from .serializers import NewsSerializer,CommentSerizlizer
from utils import restful
from .forms import PublicCommentForm
from django.db.models import Q

def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses':newses,
        'categories':categories
    }
    return render(request,'news/index.html',context=context)


def news_list(request):
    page = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end=start+settings.ONE_PAGE_NEWS_COUNT
    if category_id==0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category_id=category_id)[start:end]
    serializer = NewsSerializer(newses,many=True)
    data=serializer.data
    return restful.result(data=data)


def new_detail(request, news_id):
    news = News.objects.select_related('category','author').get(pk=news_id)

    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context=context)


def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context['newses'] = newses
    return render(request,'search/search.html',context=context)


def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')

        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())





