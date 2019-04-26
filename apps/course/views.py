from django.shortcuts import render,reverse, HttpResponse
from .models import Course
from .models import Course, CourseOrder, CourseCategory
from apps.xfzauth.decorators import xfz_login_required


# Create your views here.
def course_index(request):
    context = {
        'categories' : CourseCategory.objects.all(),
        'courses': Course.objects.all()
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
    context = {
        'course': course,
        'buyed': buyed
    }
    return render(request, 'course/course_detail.html', context=context)


def pub_course(request):
    return render(request, 'course/pub_course.html')


@xfz_login_required
def course_order(request,course_id):
    # course = Course.objects.get(pk=course_id)
    # order = CourseOrder.objects.create(course=course,buyer=request.user,status=1,amount=course.price)
    # context = {
    #     'course': course,
    #     'order': order,
    #     # /course/notify_url/
    #     'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
    #     'return_url': request.build_absolute_uri(reverse('course:course_detail',kwargs={"course_id":course.pk}))
    # }
    return HttpResponse('此功能正在研发中，您别期待了，一辈子也不可能完成的,返回上一页吧...')