from django.db import models

class Stock(models.Model):
    code = models.CharField(max_length=200)
    
    def __str__(self):
        return self.code
    
    @staticmethod
    def create_stock(code):
        stock = Stock(code=code)
        stock.save()
        return stock
        
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
    