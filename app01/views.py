#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/14 21:08
# @File    : views.py
# @Software: Pycharm
# @Author  : Changan

from django.http import HttpResponse
from django.shortcuts import render
from pymysql import *
import json
from django.core.paginator import Paginator # 分页模块
from django.http import JsonResponse
from django.core import serializers


def plabel(request):
    return render(request,'index.html')
def get_data(sql) :
    conn = connect('127.0.0.1','root','132441','aqi',charset = 'utf8')
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()
    return results

def aqi(request):# 向页面输出订单
    sql = "select * from 成都"
    m_data = get_data(sql)
    return render(request,'aqi.html',{'data':m_data})

def search(request):
    city = request.GET.get('search')
    sql = 'select * from ' + city + ''
    m_data = get_data(sql)
    date_list = []
    aqi_list = []
    pm25_list = []
    pm10_list = []
    so2_list = []
    no2_list = []
    co_list = []
    o3_list = []
    for order_list in m_data:
        date_list.append(order_list[0])
        aqi_list.append(order_list[2])
        pm25_list.append(order_list[4])
        pm10_list.append(order_list[5])
        so2_list.append(order_list[6])
        no2_list.append(order_list[7])
        co_list.append(order_list[8])
        o3_list.append(order_list[9])
    paginator = Paginator(m_data, 20)   # 显示20行数据
    pindex = request.GET.get('pindex')  # 当前页码 str类型
    if pindex == "" or pindex == None :
        pindex = 1
    page = paginator.get_page(pindex)
     # 设置前后可显示页码范围
    page_range = list(range(max(int(pindex) - 2, 1), int(pindex))) +\
                 list(range(int(pindex), min(int(pindex) + 2, page.paginator.num_pages) + 1))
    # 添加省略号标记
    if (page_range[0] - 1 >= 2) :
        page_range.insert(0, '...')
    if (page.paginator.num_pages - page_range[-1] >= 2) :
        page_range.append('...')
    # 再将第一页与最后一页始终显示
    if (page_range[0] != 1) :
        page_range.insert(0, 1)
    if (page_range[-1] != page.paginator.num_pages) :
        page_range.append(page.paginator.num_pages)

    context = {
        'page' : page,
        'city' : city,
        'page_range' : page_range,
        'date_list' : json.dumps(date_list),
        'aqi_list' : json.dumps(aqi_list),
        'pm25_list' : json.dumps(pm25_list),
        'pm10_list' : json.dumps(pm10_list),
        'so2_list' : json.dumps(so2_list),
        'no2_list' : json.dumps(no2_list),
        'co_list' : json.dumps(co_list),
        'o3_list' : json.dumps(o3_list),

    }
    return render(request, 'city.html', {'context':context})

def city(request):
    post_data = json.loads(request.body)
    city = post_data.get('cityname')
    print(city)
    sql = 'select * from ' + city + ''
    # sql = "select * from 成都"
    m_data = get_data(sql)
    date_list = []  # 时间
    aqi_list = []
    for order_list in m_data :
        date_list.append(order_list[0])
        aqi_list.append(order_list[2])
    paginator = Paginator(m_data, 20)  # 显示20行数据
    pindex = request.GET.get('pindex')  # 当前页码 str类型
    if pindex == "" or pindex == None :
        pindex = 1
    page = paginator.get_page(pindex)
    # 设置前后可显示页码范围
    page_range = list(range(max(int(pindex) - 2, 1), int(pindex))) + \
                 list(range(int(pindex), min(int(pindex) + 2, page.paginator.num_pages) + 1))
    # 添加省略号标记
    if (page_range[0] - 1 >= 2) :
        page_range.insert(0, '...')
    if (page.paginator.num_pages - page_range[-1] >= 2) :
        page_range.append('...')
    # 再将第一页与最后一页始终显示
    if (page_range[0] != 1) :
        page_range.insert(0, 1)
    if (page_range[-1] != page.paginator.num_pages) :
        page_range.append(page.paginator.num_pages)
    context = {
        'page' : page,
        'city' : city,
        'page_range' : page_range,
        'date_list' : json.dumps(date_list),
        'aqi_list' : json.dumps(aqi_list),
    }
    return render(request, 'city.html', {'context':context})