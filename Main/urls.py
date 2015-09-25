from django.conf.urls import include, url
from django.http import HttpResponseRedirect

def redirect(request):
    return HttpResponseRedirect("/stocks/stocks")

urlpatterns = [
    url(r'^stocks/', include('Stocks.urls')),
    url(r'^.*$', redirect),
]