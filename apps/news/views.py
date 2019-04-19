from django.shortcuts import render
from .models import NewsCategory,News
from django.conf import settings
from .serializers import NewsSerializer
from utils import restful

def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.order_by('-pub_time')[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses':newses,
        'categories':categories
    }
    return render(request,'news/index.html',context=context)


def news_list(request):
    page =int(request.GET.get('p',1))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end=start+settings.ONE_PAGE_NEWS_COUNT

    newses = News.objects.order_by('-pub_time')[start:end]
    serializer = NewsSerializer(newses,many=True)
    data=serializer.data
    return restful.result(data=data)



def new_detail(request,news_id):
    return render(request,'news/news_detail.html')


def search(request):
    return render(request,'search/search.html')




