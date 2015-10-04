from django.conf.urls import include, url
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render


def redirect(request):
    return HttpResponseRedirect("/stocks/stocks")

def robots(request):
    return HttpResponse("<pre>User-agent: *\nDisallow: /</pre>")

def main(request):
    return render(request, 'home.html', {})

urlpatterns = [
    url(r'^robots.txt$', robots),          
    url(r'^stocks/', include('Stocks.urls')),
    url(r'^.*$', main),
]