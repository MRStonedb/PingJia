#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-3-8
# Copyright (c) 2018 $USER.ALL rights reserved.
from django.conf.urls import url,include
from . import views

urlpatterns = [
    # url('^$',views.register),
    url('register/',views.register),
    url('register_handle',views.register_handle),
    # url('active/',views.active),

    url('login/',views.login),
    url(r'^yzm/$', views.verify_code),
    url('login_handle',views.login_handle),

    url('logout',views.logout),
]