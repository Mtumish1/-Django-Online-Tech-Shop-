from django.shortcuts import render
from .models import Category, Product



# Create your views here. Create a view to list all the products or filter products by a given category


def product_list(request, category_slug=None):
    categ