from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from reuters_library import ReutersLibrary 
from Stocks import models

def add_stock_request(request):
    code = request.GET.get('stock')
    add_stock(code)
    return HttpResponseRedirect("/stocks/stocks")

def add_stock(code):
    if code is not None:
        try:
            models.Stock.objects.get(code=code)
        except models.Stock.DoesNotExist:
            models.Stock.create_stock(code)

def add_category_request(request):
    name = request.GET.get('category')
    add_category(name)
    return HttpResponseRedirect("/stocks/stocks")
    
def add_category(name):
    if name is not None:
        try:
            models.Category.objects.get(name=name)
        except models.Category.DoesNotExist:
            models.Category.create_category(name)

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
        dictionary = ReutersLibrary.get_stock_values(code)
        try:
            stock = models.Stock.objects.get(code=code)
        except models.Stock.DoesNotExist:
            return HttpResponseRedirect("/stocks/stocks")
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
            pass
        return HttpResponse(json.dumps(dictionary))
    except models.Stock.DoesNotExist:
        return HttpResponse("[]")

def stocks(request):
    return render(request, 'stocks.html', {})

def stock_list(request):
    category_name = request.GET.get('category')
    stocks = models.Stock.objects.all()
    if category_name is not None:
        try:
            category = models.Category.objects.get(name=category_name)
            category_stocks = models.CategoryStock.objects.filter(category_id=category.pk)
            stocks = []
            for category_stock in category_stocks:
                try: 
                    stock = models.Stock.objects.get(pk=category_stock.stock_id)
                    stocks.append(stock)
                except models.Stock.DoesNotExist:
                    pass
        except models.Category.DoesNotExist:
            pass
        except models.CategoryStock.DoesNotExist:
            stocks = []
    response = []
    for stock in stocks:
        response.append(stock.code)
    response.sort()
    return HttpResponse(json.dumps(response))

def categories(request):
    categories = models.Category.objects.all()
    response = []
    for category in categories:
        response.append(category.name)
    response.sort()
    return HttpResponse(json.dumps(response))

def associate_stock_with_categories_request(request):
    code = request.GET.get('stock')
    category_name = request.GET.get('category')
    associate_stock_with_categories(code, category_name)
    return HttpResponseRedirect("/stocks/stocks")

def associate_stock_with_categories(code, category_name): 
    if code is None or category_name is None:
        return
    try:
        stock = models.Stock.objects.get(code=code)
    except models.Stock.DoesNotExist:
        return
    try:
        category = models.Category.objects.get(name=category_name)
    except models.Category.DoesNotExist:
        return
    
    models.CategoryStock.create_category_stock(category.pk, stock.pk)

def disassociate_stock_with_categories_request(request):
    code = request.GET.get('stock')
    category_name = request.GET.get('category')
    disassociate_stock_with_categories(code, category_name)
    return HttpResponseRedirect("/stocks/stocks")
    
def disassociate_stock_with_categories(code, category_name):
    if code is None or category_name is None:
        return
    try:
        stock = models.Stock.objects.get(code=code)
    except models.Stock.DoesNotExist:
        return
    try:
        category = models.Category.objects.get(name=category_name)
    except models.Category.DoesNotExist:
        return
    try:
        category_stocks = models.CategoryStock.objects.filter(stock_id=stock.pk,
                                                           category_id=category.pk)
        for category_stock in category_stocks:
            category_stock.delete()
    except models.CategoryStock.DoesNotExist:
        pass

def disassociate_stock_from_category_request(request):
    category_name = request.GET.get('category')
    disassociate_stock_from_category(category_name)
    return HttpResponseRedirect("/stocks/stocks")

def disassociate_stock_from_category(category_name):    
    try:
        category = models.Category.objects.get(name=category_name)
    except models.Category.DoesNotExist:
        return
    try:
        category_stocks = models.CategoryStock.objects.filter(category_id=category.pk)
        for category_stock in category_stocks:
            category_stock.delete()
    except models.CategoryStock.DoesNotExist:
        pass

def add_stocks(stock_list, category):
    disassociate_stock_from_category(category)
    add_category(category)
    for stock in stock_list:
        add_stock(stock)
        associate_stock_with_categories(stock, category)

def update_nzx_50(request):
    stocks = ReutersLibrary.get_NZX_50()
    add_stocks(stocks, "nzx_50")
    return HttpResponseRedirect("/stocks/stocks")
    
def update_nzx(request):
    stocks =  ReutersLibrary.get_NZX()
    add_stocks(stocks, "nzx")
    return HttpResponseRedirect("/stocks/stocks")