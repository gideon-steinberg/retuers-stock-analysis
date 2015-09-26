from django.db import models
from django.utils import timezone
from Stocks.reuters_library import ReutersLibrary

class Stock(models.Model):
    code = models.CharField(max_length=200)
    
    def __str__(self):
        return self.code
    
    @staticmethod
    def create_stock(code):
        stock = Stock(code=code)
        stock.save()
        return stock
    
    def create_stock_value(self):
        values = ReutersLibrary.get_stock_values(self.code)
        if len(values) > 7:
            return StockValue.create_stock_value(self.pk, values[0], values[1],
                                                 values[2], values[3], values[4],
                                                 values[5], values[6],values[7],
                                                 values[8], values[9], values[10],
                                                 values[11])
        return None
    
class StockValue(models.Model):
    stock_id = models.CharField(max_length=200)
    buy = models.IntegerField()
    outperform = models.IntegerField()
    hold = models.IntegerField()
    underperform = models.IntegerField()
    sell = models.IntegerField()
    no_opinion = models.IntegerField()
    mean = models.FloatField()
    mean_last_month=models.FloatField()
    consensus = models.CharField(max_length=200)
    dividend = models.CharField(max_length=200)
    price_earnings = models.CharField(max_length=200)
    time = models.TimeField()
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.id
    
    @staticmethod
    def create_stock_value(stock_id, buy, outperform, hold, underperform, sell,
                           no_opinion, mean, mean_last_month, consensus, dividend,
                           price_earnings, description):
        stock_value = StockValue(stock_id=stock_id, buy= buy, outperform= outperform,
                                 hold= hold, underperform=underperform, sell= sell,
                                 no_opinion= no_opinion,mean= mean, mean_last_month=mean_last_month,
                                 consensus=consensus, dividend=dividend, price_earnings=price_earnings,
                                 time= timezone.now(), description=description)
        stock_value.save()
        return stock_value
    
    def get_stock_code(self):
        stock = Stock.objects.get(pk=self.stock_id)
        return stock.code
    
    def get_mean_difference(self):
        difference = float(self.mean) - float(self.mean_last_month)
        if difference == 0:
            difference = ""
        else:
            # formatting......
            difference = float(format(difference, '.4f'))
        return difference
    
    @staticmethod
    def update_stock_values():
        stocks = Stock.objects.all()
        for stock in stocks:
            stock.create_stock_value()
                
    def get_row_style(self):
        style = ""
        if self.mean <= 2:
            style = style + "background-color:#00ff00;"
        if self.mean >= 3:
            style = style + "background-color:#ff0000;color: #ffffff;"
        if self.get_mean_difference() <= -1:
            style = style + "font-weight: bold;"
        return style
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def create_category(name):
        category = Category(name=name)
        category.save()
        return category
    
class CategoryStock(models.Model):
    category_id = models.CharField(max_length=200)
    stock_id = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def create_category_stock(category_id, stock_id):
        category_stock = CategoryStock(category_id=category_id, stock_id=stock_id)
        category_stock.save()
        return category_stock
    