from .cart import Cart 


def cart(request):
    return {'cart': Cart(request)}


    #instantiate the cart using the request object and make it available for the templates as a variable named cart.