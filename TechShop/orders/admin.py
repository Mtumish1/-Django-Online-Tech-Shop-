from django.contrib import admin
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'city', 'area', 'estate',
    'paid', 'created', 'updated']
    inlines = [OrderItemInline]


    