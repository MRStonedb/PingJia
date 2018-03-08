from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.

# 视图用于展示输入框，获取用户输入的信息
def index(request):
    context = {'title': '首页', 'info': '欢迎使用月嫂评价查询系统,请输入需要查询的月嫂姓名'}
    return render(request, 'yuesao_pingjia/index.html', context)


# 视图用于处理获取的数据，返回符合要求的数据
def search(request):
    dict = request.POST
    name = dict.get('yuesao_name')

    yuesao = pingjia_info.objects.filter(name=name).count()
    if yuesao == 0:
        return HttpResponse('抱歉，没有这个月嫂')
    else:
        yuesao = pingjia_info.objects.filter(name=name)
        context = {'title':'查询','yuesao':yuesao}
        return render(request, 'yuesao_pingjia/yuesao.html', context)

