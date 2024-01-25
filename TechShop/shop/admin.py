from django.contrib import admin
from .models import Category, Product




# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name')}




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available',] #the list_editable attribute in the ProductAdmin class to set the fields that can be edited from the list display page of the administration site
    prepopulated_fields = {'slug': ('name',)}