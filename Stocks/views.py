from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from Stocks import models

def add_stock(request):
    code = request.GET.get('stock')
    if code is not None:
        try:
            models.Stock.objects.get(code=code)
        except models.Stock.DoesNotExist:
            models.Stock.create_stock(code)
    return HttpResponseRedirect("/stocks/stocks")

def add_category(request):
    name = request.GET.get('category')
    if name is not None:
        try:
            models.Category.objects.get(name=name)
        except models.Category.DoesNotExist:
            models.Category.create_category(name)
    return HttpResponseRedirect("/stocks/stocks")

def remove_stock(request):
    code = request.GET.get('stock')
    if code is not None:
        try:
            stock = models.Stock.objects.get(code=code)
            stock.delete()
        except models.Stock.DoesNotExist:
            pass
    return HttpResponseRedirect("/stocks/stocks")

def stock_info(request):
    code = request.GET.get('stock')
    if code is None:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        stock = models.Stock.objects.get(code=code)
        stock_value = stock.create_stock_value()
        dictionary = {}
        dictionary["code"] = stock.code
        if stock_value == None:
            return HttpResponse(json.dumps(dictionary))
        dictionary["description"] = stock_value.description
        dictionary["buy"] = stock_value.buy
        dictionary["outperform"] = stock_value.outperform
        dictionary["hold"] = stock_value.hold
        dictionary["underperform"] = stock_value.underperform
        dictionary["sell"] = stock_value.sell
        dictionary["mean"] = stock_value.mean
        dictionary["mean_difference"] = stock_value.get_mean_difference()
        dictionary["consensus"] = stock_value.consensus
        dictionary["dividend"] = stock_value.dividend
        dictionary["price_earnings"] = stock_value.price_earnings
        return HttpResponse(json.dumps(dictionary))
    except models.Stock.DoesNotExist:
        return HttpResponse("[]")

def stocks(request):
    stocks = models.Stock.objects.all()
    context = {'stocks' : stocks}
    return render(request, 'stocks.html', context)

def stock_list(request):
    stocks = models.Stock.objects.all()
    response = []
    for stock in stocks:
        response.append(stock.code)
    return HttpResponse(json.dumps(response))

def categories(request):
    categories = models.Category.objects.all()
    response = []
    for category in categories:
        response.append(category.name)
    return HttpResponse(json.dumps(response))

def associate_stock_with_categories(request):
    code = request.GET.get('stock')
    category_name = request.GET.get('category')
    if code is None or category_name is None:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        stock = models.Stock.objects.get(code=code)
    except models.Stock.DoesNotExist:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        category = models.Category.objects.get(code=code)
    except models.Category.DoesNotExist:
        return HttpResponseRedirect("/stocks/stocks")
    
    models.CategoryStock.create_category_stock(category.pk, stock.pk)
    return HttpResponseRedirect("/stocks/stocks")

def disassociate_stock_with_categories(request):
    code = request.GET.get('stock')
    category_name = request.GET.get('category')
    if code is None or category_name is None:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        stock = models.Stock.objects.get(code=code)
    except models.Stock.DoesNotExist:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        category = models.Category.objects.get(code=code)
    except models.Category.DoesNotExist:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        category_stock = models.CategoryStock.objects.get(stock_id=stock.pk,
                                                           category_id=category.pk)
        category_stock.delete()
    except models.CategoryStock.DoesNotExist:
        pass
    return HttpResponseRedirect("/stocks/stocks")
