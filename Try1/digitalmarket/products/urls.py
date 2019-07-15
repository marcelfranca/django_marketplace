from django.urls import path, re_path
from . import views
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView


app_name = 'products'

urlpatterns = [
    path('create/', views.create_view, name='create_view'),
    path('', ProductListView.as_view(), name='list'),
    path('add/', ProductCreateView.as_view(), name='create'),
    re_path(r'^detail/(?P<object_id>\d+)/$', views.detail_view, name='detail'),
    re_path(r'^product/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update'),
    re_path(r'^slug/(?P<slug>[\w-]+)/$', views.detail_slug_view, name='detail_slug'),
    re_path(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail_view'),
    re_path(r'^product/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),

]
