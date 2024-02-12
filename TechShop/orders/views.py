from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created



def order_create(request):
    cart = Cart (request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                price =item['price'], quantity=item['quantity'])


            # clear cart after order confirmation
            
            cart.clear()
            order_created.delay(order.id) # Launch asynchronous task by calling the delay() method of the task
            
            # set the order in the session
            request.session['order_id'] = order.id

            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render (request, 'orders/order/create.html', {'cart': cart, 'form': form})