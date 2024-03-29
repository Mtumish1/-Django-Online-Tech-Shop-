from django.db import models
from shop.models import Product



class Order(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=250)
    estate = models.CharField(max_length=250)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    paid = models.BooleanField(default=False) #  This field differentiates between paid and unpaid orders
    braintree_id = models.CharField(max_length=150, blank=True) # This will allow you to link each order with its related Braintree transaction.



    class Meta:
        ordering = ('-created',)

    def __str__ (self):
        return f'Order{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)


    def get_cost(self):
        return self.price * self.quantity

