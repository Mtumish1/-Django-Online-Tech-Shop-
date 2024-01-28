from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import  require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# This is the view for adding products to the cart or updating quantities for existing products.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

# A view to remove items from the cart.

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404 (Product, id=product_id) #receives the product ID as a parameter
    cart.remove(product)
    return redirect('cart:cart_detail')


    #A view to display the cart and its items

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})