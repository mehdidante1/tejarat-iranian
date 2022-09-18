from multiprocessing import context
from .models import *
from django.shortcuts import render
from django.db.models import Min , Max

def get_filters(request):
    cats = Product.objects.distinct().values('category__title' , 'category__id')
    brands = Product.objects.distinct().values('brand__title' , 'brand__id')
    colors = ProductAttribute.objects.distinct().values('color__title' , 'color__id' , 'color__color_code')
    minMaxPrice = ProductAttribute.objects.aggregate(Min('price') , Max('price'))
    data = {
        "category" : cats , 
        "brand" : brands ,
        "color" : colors , 
        "minMaxPrice" : minMaxPrice
    }
    return data

