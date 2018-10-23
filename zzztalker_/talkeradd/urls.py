from django.urls import path
from . import views

urlpatterns = [
    path('bg-manage-add/', views.index),
    path('add/',views.add),

]
