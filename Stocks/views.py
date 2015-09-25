from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from Stocks import models

def add_stock(request):
    code = request.GET.get('stock')
    try:
        models.Stock.objects.get(code=code)
    except models.Stock.DoesNotExist:
        models.Stock.crete_stock(code)
    return HttpResponseRedirect("/stocks/stocks")

def remove_stock(request):
    code = request.GET.get('stock')
    try:
        stock = models.Stock.objects.get(code=code)
        stock.delete()
    except models.Stock.DoesNotExist:
        pass
    return HttpResponseRedirect("/stocks/stocks")

def stock_info(request):
    code = request.GET.get('stock')
    try:
        stock = models.Stock.objects.get(code=code)
        stock_value = stock.create_stock_value()
        if stock_value == None:
            return HttpResponse("[]")
        dictionary = {}
        dictionary["code"] = stock.code
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
    models.StockValue.update_stock_values()
    stocks = models.Stock.objects.all()
    stock_values = []
    for stock in stocks:
        stock_value = models.StockValue.objects.filter(stock_id=stock.pk).order_by("time").last()
        if stock_value != None:
            stock_values.append(stock_value)
    context = {'stock_values': stock_values}
    return render(request, 'stocks.html', context)