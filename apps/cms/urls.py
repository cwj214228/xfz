from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import course_views

app_name = 'cms'
urlpatterns = [
    path('', views.index, name='index'),
    path('write_news/', views.WriteNewsView.as_view(), name='write_news'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_news_category/', views.add_news_category, name='add_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news_category'),
    path('delete_news_category/', views.delete_news_category, name='delete_news_category'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('qntoken/', views.qntoken, name='qntoken'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# 这是课程相关的url映射
urlpatterns += [
    path('pub_course/',course_views.PubCourse.as_view(),name='pub_course')
]
