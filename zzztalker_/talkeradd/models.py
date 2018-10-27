from django.db import models
from mongoengine import *
# Create your models here.
class Counters(Document):
    _id = StringField()
    seq_value = IntField()
    @classmethod
    def addCounters(cls, _id, seq_value):
        coun = cls(_id=_id, seq_value=seq_value)
        return coun;

class Foodnews(Document):
    _id =IntField()
    title = StringField(max_length=30)
    content = StringField(max_length=300)
    category = StringField(max_length=20)
    images = StringField(max_length=20)
    foodstarttime =DateTimeField()
    @classmethod
    def addFoodnews(cls, _id, title, content, category, images):
        foodnews = cls(_id=_id, title=title, content=content, category=category, images=images, foodstarttime='2018/10/10')
        return foodnews;