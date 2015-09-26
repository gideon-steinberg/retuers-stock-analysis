from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_stock$', views.add_stock, name='add_stock'),
    url(r'^add_category$', views.add_category, name='add_category'),
    url(r'^remove_category$', views.remove_category, name='remove_category'),
    url(r'^remove_stock$', views.remove_stock, name='remove_stock'),
    url(r'^stocks$', views.stocks, name='stocks'),
    url(r'^stock_list$', views.stock_list, name='stock_list'),
    url(r'^categories$', views.categories, name='categories'),
    url(r'^associate_stock_with_categories$', 
        views.associate_stock_with_categories, 
        name='associate_stock_with_categories'),
    url(r'^disassociate_stock_with_categories$', 
        views.disassociate_stock_with_categories, 
        name='disassociate_stock_with_categories'),
    url(r'^stock_info$', views.stock_info, name='stock_info'),
]