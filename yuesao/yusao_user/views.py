# Create your views here.
from django.shortcuts import render,redirect
from hashlib import sha1
from .models import *
# from . import task
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont


def register(request):
    context = {'title': '注册',}
    return render(request, 'yuesao_user/register.html', context)

def register_handle(request):
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    uphone = dict.get('phone')

    # 对密码进行加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd_sha1 = s1.hexdigest()

    # 创建对象，调用save方法将数据存入数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.uphone = uphone
    user.save()

    # task.sendmail.delay(user.id, uemail)
    # return HttpResponse('注册成功，请到邮箱激活')
    uid = user.id
    user = UserInfo.objects.get(id=uid)
    user.isActive = 1  # 或者等于ture也可以
    user.save()
    # return redirect('/user/active/',1)
    return HttpResponse('激活成功,<a href="/user/login/">点击登录</a>')


# def active(request,uid):
#     # 激活账户，因为userinfo类里定义了isactive属性，这里只需要用户点击邮箱的链接，
#     # 然后把isactive修改为1（默认0），就可以实现激活
#     # 因为在邮箱的链接里已经有用户id这个参数，所以这里也需要接收uid
#     user = UserInfo.objects.get(id=uid)
#     user.isActive = 1  # 或者等于ture也可以
#     user.save()
#     # 激活成功转到登录页面
#     return HttpResponse('激活成功,<a href="/user/login/">点击登录</a>')



def login(request):
    context = {'title': '登录', }
    return render(request, 'yuesao_user/login.html', context)

def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # 内存文件操作(python2)
    # import cStringIO
    # buf = cStringIO.StringIO()

    # 内存文件操作(python3)
    from io import BytesIO
    buf = BytesIO()

    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def login_handle(request):
    # 需要确认是否是post请求，如果不是，则重新转到登录页
    if request.method != 'POST':
        return redirect('/user/login/')
    dict = request.POST
    # username是模板里form表单里的name决定的，和数据库里的uname不同
    uname = dict.get('username')
    upwd = dict.get('pwd')
    # urem = dict.get('remember', '0')
    context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'uname_error': 0, 'upwd_error': 0}
    # 从数据库中取到uname的用户名
    user = UserInfo.objects.filter(uname=uname)
    # 判断用户名是否存在
    if len(user) == 0:
        context['uname_error'] = 1
        return redirect('/user/login/', context)
    else:
        # 说明用户名存在，对比密码
        upwd_db = user[0].upwd  # 取出数据库中用户名为uname的第一个的密码（有可能重名）

        # 对用户填写的密码加密
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        upwd_sha1 = s1.hexdigest()

        # 对比密码
        if upwd_db == upwd_sha1:
            # 判断是否激活
            if user[0].isActive:  # 相当于user【0】.isactive == ture
                # 记录请求之前的路径，middleware
                response = redirect(request.session.get('url_path', '/'))
                # 判断用户是否选择了记住密码
                # if urem == 1:  # 用户选择了记住密码
                #     response.set_cookie('uname', uname, expires=60 * 60 * 24 * 15)
                # # 如果没有选择，把过期事件改为-1，退出后立马删除cookie
                # else:
                #     response.set_cookie('uname', '', expires=-1)

                # 在这里记住用户的id和用户名，是为了方便其他网页识别当前这个用户是否已经登录
                # 如果不记录，其他页面不能确定你是否已经登录（重点）
                request.session['uid'] = user[0].id
                request.session['uname'] = uname
                return response
            else:
                return HttpResponse('账户未激活，请到邮箱激活')

        else:
            context['upwd_error'] = 1
            return render(request, 'yuesao_user/login.html', context)
    # return redirect('/')


def logout(request):
    # 登录状态存储在session中，清除session就可以退出
    request.session.flush()
    return redirect('/')