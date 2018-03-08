#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-3-7
# Copyright (c) 2018 $USER.ALL rights reserved.
from django.conf.urls import url,include
from . import views


urlpatterns = [
    # url(r'^$', include('yusao_pingjia.urls')),
    url('^$', views.index),
    url('^search/$',views.search),
]