from django.urls import path, re_path
from . import views

app_name = 'products'

urlpatterns = [
    # path('detail/', views.detail_view, name='detail'),
    # path('list/', views.list_view, name='list')
    re_path(r'^detail/(?P<object_id>\d+)/$', views.detail_view, name='detail_view'),
    re_path(r'^slug/(?P<slug>[\w-]+)/$', views.detail_slug_view, name='detail_slug_view'),
    re_path(r'^list/$', views.list_view, name='list_view'),

]