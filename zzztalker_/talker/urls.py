from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexHome4dianzan),
    path('index-home/', views.indexHome4dianzan),
    path('index-network/', views.indexNetwork),
    path('index-blog/', views.indexBlog),
    path('index-other/', views.indexOther),
    path('bg-manage/', views.bgManage),
    path('bg-manage-show/', views.bgManageShow),
    path('bg-manage-delete/', views.bgManageDelete),
    path('bg-manage-update/', views.bgManageUpdate),
    path('update/', views.bgUpdate),
    path('showAjax/', views.showAjax),
    path('index-search/', views.indexSearch),
    path('user-login-index/', views.userLoginIndex),
    path('user-login/', views.userLogin),
    path('user-login-out/', views.userLoginOut),

]
