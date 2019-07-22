from django.urls import path, re_path
from . import views


app_name = 'products'

urlpatterns = [
    re_path(r'^detail/$', views.detail_view, name='detail_view'),
    re_path(r'^list/$', views.list_view, name='list_view'),
]
