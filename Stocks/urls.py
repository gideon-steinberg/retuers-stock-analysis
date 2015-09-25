from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_stock$', views.add_stock, name='add_stock'),
    url(r'^remove_stock$', views.remove_stock, name='remove_stock'),
    url(r'^stocks$', views.stocks, name='stocks'),
    url(r'^stock_info', views.stock_info, name='stock_info'),
]