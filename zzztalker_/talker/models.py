from django.db import models
from mongoengine import *
import datetime
# Create your models here.
# 模拟实现MongoDB中id的自增长的数据模型
class Counters(Document):
    _id = StringField()
    seq_value = IntField()
    @classmethod
    def addCounter(cls, _id, seq_value):
        coun =cls(_id=_id, seq_value=seq_value)
        return coun;

# 信息模型
class Foodnews(Document):
    title = StringField(max_length=30)
    content = StringField(max_length=200)
    category = StringField(max_length=20)
    images =StringField(max_length=20)
    foodstarttime = DateTimeField()
    @classmethod
    def addFoodnews(cls, _id, title, content, category, images):
        foodnews = cls(_id=_id, title=title, content=content, category=category, images=images,foodstarttime='2018/10/10')
        return foodnews;

# 点赞功能
class Dianzan(Document):
    title_id =IntField()
    count_num =IntField(default=0)
    @classmethod
    def addDianzan(cls, title_id, count_num):
        dianzan =cls(title_id=title_id, count_num=count_num)
        return dianzan

# 联合查询表
class Fooddianzan(Document):
    title = StringField(max_length=30)
    content = StringField(max_length=200)
    category = StringField(max_length=20)
    images = StringField(max_length=20)
    title_id = IntField()
    count_num = IntField(default=0)
    @classmethod
    def addFooddianzan(cls, title, content, category, images, title_id, count_num):
        fooddianzan = cls(title=title, content=content, category=category, images=images, title_id=title_id
                          , count_num=count_num)
        return fooddianzan

# 用户表
class User(Document):
    username = StringField(max_length=30)
    password = StringField(max_length=30)
    urole = StringField(max_length=30)
    ustatus = IntField(default=0)
    @classmethod
    def addUser(cls, username, password, urole, ustatus):
        user = cls(username=username, password=password, urole=urole, ustatus=ustatus)
        return user