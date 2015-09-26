from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from reuters_library import ReutersLibrary 
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

def remove_category(request):
    category_name = request.GET.get('category')
    if category_name is not None:
        try:
            category = models.Category.objects.get(name=category_name)
            category.delete()
        except models.Category.DoesNotExist:
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
            base_response = ReutersLibrary.get_response(stock.code)
            dictionary["description"] = base_response.xpath(ReutersLibrary.DESCRIPTION_XPATH)[0]
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
        
        try:
            category_stocks = models.CategoryStock.objects.filter(stock_id=stock.pk)
            categories = []
            for category_stock in category_stocks:
                try:
                    category = models.Category.objects.get(pk=category_stock.category_id)
                    categories.append(category.name)
                except models.Category.DoesNotExist:
                    pass
            dictionary["categories"] = categories
        except models.CategoryStock.DoesNotExist:
            base_response = ReutersLibrary.get_response(stock.code)
            dictionary = {}
            dictionary["code"] = stock.code
            dictionary["description"] = base_response.xpath(ReutersLibrary.DESCRIPTION_XPATH)[0]
            return HttpResponse(json.dumps(dictionary))
        return HttpResponse(json.dumps(dictionary))
    except models.Stock.DoesNotExist:
        return HttpResponse("[]")

def stocks(request):
    return render(request, 'stocks.html', {})

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
        category = models.Category.objects.get(name=category_name)
    except models.Category.DoesNotExist:
        return HttpResponseRedirect("/stocks/stocks")
    
    try:
        models.CategoryStock.objects.get(stock_id=stock.pk, category_id=category.pk)
    except models.CategoryStock.DoesNotExist:
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
        category = models.Category.objects.get(name=category_name)
    except models.Category.DoesNotExist:
        return HttpResponseRedirect("/stocks/stocks")
    try:
        category_stocks = models.CategoryStock.objects.filter(stock_id=stock.pk,
                                                           category_id=category.pk)
        for category_stock in category_stocks:
            category_stock.delete()
    except models.CategoryStock.DoesNotExist:
        pass
    return HttpResponseRedirect("/stocks/stocks")
