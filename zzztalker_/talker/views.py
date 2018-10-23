from django.shortcuts import render, HttpResponse, redirect
from .models import Counters, Foodnews, Dianzan, Fooddianzan

# Create your views here.
import redis
conn = redis.Redis(host='localhost', port=6379)

# 主页
def indexHome4dianzan(request):
    list = Foodnews.objects.all()
    for i in list:
        title = i.title
        content = i.content
        category = i.category
        images = i.images
        # 根据总记录数，在联合表中添加新的记录
        if not Fooddianzan.objects.filter(title_id=i.pk):
            title_id = i.pk
            count_num = 0
            obj = Fooddianzan.addFooddianzan(title, content, category, images, title_id, count_num)
            obj.save()
    all_list = Fooddianzan.objects.all()
    pageid = request.GET.get('page')
    obj = MyPaginator(all_list, 3, pageid, 4)
    currentPage = obj.get_page(pageid)
    # 通过点赞数显示热门文章
    my_docs =[]
    for i in Fooddianzan.objects.all().order_by('-count_num'):
        if i.count_num !=0:
            my_docs.append({'title' : i.title, 'dianzan' : i.count_num})
    # 天气
    listTem = showWeather()
    return render(request, 'talker/index-home.html', {'list' : currentPage, 'my_docs': my_docs, 'lt': listTem})

# 简单的模型
from django.core.paginator import Paginator
class MyPaginator(Paginator):
    def __init__(self, object_list, per_page, currentPage, showPage, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.currentPage =1 if currentPage ==None else currentPage
        self.showPage =showPage
    def _query_range_exd(self):
        for i in range(self.num_pages + 1):
            if int(self.currentPage) < 3:
                return range(1, self.num_pages + 1)[0 : self.showPage]
            else:
                if self.num_pages + 1 - int(self.currentPage) < self.showPage:
                    return range(self.num_pages + 1 - self.showPage, self.num_pages + 1)[0 : self.showPage]
                else:
                    return range(int(self.currentPage) - 2, self.num_pages + 1)[0 : self.showPage]
    query_range_exd =property(_query_range_exd)

# 后台基础管理页面
def bgManage(request):
    return render(request, 'talker/bg-manage-base.html')

# 后台展示数据
def bgManageShow(request):
    list = Foodnews.objects.all()
    return render(request, 'talker/bg-manage-show.html', {'list' : list})

# 后台删除数据
def bgManageDelete(request):
    ttitle = request.GET.get('title');
    tcategory = request.GET.get('category')
    Foodnews.objects.filter(title=ttitle, category=tcategory).delete()
    temp_list = Foodnews.objects.all()
    return render(request, 'talker/bg-manage-show.html', {'list' : temp_list})

# 后台修改数据
def bgManageUpdate(request):
    title = request.GET.get('title')
    category = request.GET.get('category')
    myobj = Foodnews.objects.all().filter(title=title, category=category)[0]
    conn.set('title', title)
    conn.set('category', category)
    conn.set('theid', myobj.pk)
    # request.session['update_obj'] = myobj # 需要重新配置，版本不支持
    return render(request, 'talker/bg-manage-update.html', {'obj': myobj})

def bgUpdate(request):
    if request.method == 'POST':
        # obj = request.session.get('update_obj')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        images = request.POST.get('images')
        # f = Foodnews.addFoodnews(title, content, category, images)
        # f.save()
        ti = conn.get('title').decode()
        ca = conn.get('category').decode()
        theid = conn.get('theid').decode()
        # myobj = Foodnews.objects.all().filter(title=ti, category=ca)[0]
        myobj = Foodnews.objects.filter(title=ti, category=ca)\
            .update(title=title, content=content, category=category, images=images)
        temp_list =Foodnews.objects.all()
    return render(request, 'talker/bg-manage-show.html', {'list': temp_list})

# 简单的点赞功能实现
# 1）主页面的点赞
import json
def showAjax(request):
    if request.is_ajax():
        title_id = request.GET.get('title_id')
        # 计数
        if Dianzan.objects.filter(title_id=title_id):
            temp =Dianzan.objects.filter(title_id=title_id)[0].count_num + 1
            obj =Dianzan.objects.filter(title_id=title_id)[0].update(count_num=temp)
        else:
            obj = Dianzan.addDianzan(title_id, 1)
            obj.save()
        if Fooddianzan.objects.filter(title_id=title_id):
            Fooddianzan.objects.filter(title_id=title_id)\
                .update(count_num=Dianzan.objects.filter(title_id=title_id)[0].count_num)
        ret = {'the_id' : Dianzan.objects.filter(title_id=title_id)[0].count_num}
        return HttpResponse(json.dumps(ret))
    else:
        return redirect('/index-home/')

# 简单的搜索实现
# 1）根据内容
from django.db.models import Q
def indexSearch(request):
    mysearch = request.GET.get('mysearch')
    if mysearch != '':
        list = Foodnews.objects.filter(content__icontains=mysearch)
        return render(request, 'talker/index-search.html', {'list' : list})
    return redirect('/index-home/')

# 简单的天气预报实现
# 中国天气网：http://www.weather.com.cn/robots.txt
# User-agent: *
# Allow: /

import bs4
from bs4 import BeautifulSoup
import requests
def showWeather():
    currentCity = ''
    tem = ''
    minTem =''
    maxTem = ''
    fengxiang = ''
    fengli = ''
    list = []
    url = 'http://www.weather.com.cn/weather1d/101200101.shtml'
    r =requests.get(url)
    r.raise_for_status()
    r.encoding =r.apparent_encoding
    html =r.text
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find(class_='xyn-weather-box'):
        if i.name =='h2':
            currentCity =i.span.text
    for i in soup.find(class_='t').ul:
        if not isinstance(i, bs4.element.NavigableString):
            if '白天' in i.h1.text:
                tem = i.find(class_='wea').text
                maxTem = '%s ℃' % i.find(class_='tem').span.text
                fengxiang = i.find(class_='win').span['title']
                fengli = i.find(class_='win').span.text
            if '夜间' in i.h1.text:
                minTem = '%s ℃' % i.find(class_='tem').span.text
    list.append({'currentCity' : currentCity,
                 'tem' : tem,
                 'minTem' : minTem,
                 'maxTem' : maxTem,
                 'fengxiang' : fengxiang,
                 'fengli' : fengli})
    return list

def indexNetwork(request):
    return render(request, 'talker/index-network.html')

def indexBlog(request):
    return render(request, 'talker/index-blog.html')

def indexOther(request):
    return render(request, 'talker/index-other.html')