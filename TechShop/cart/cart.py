from django.conf import settings
from decimal import Decimal
from shop.models import Product




# This Cart class that will allow you to manage the shopping cart

class Cart(object):
    def __init__(self, request):
        self.session = request.session #You store the current session using self.session = request.session to make it accessible to the other methods of the Cart class.
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session [settings.CART_SESSION_ID]
        self.cart = cart


#You requirethe cart to be initialized with a request object. 
# You store the current session using self.session = request.session
#  to make it accessible to the other methods of the Cart class

    
    def add (self, product, quantity=1, override_quantity=False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # A method for saving products in the cart

    def save(self):
        self.session.modified = True

   # A method for removing products from the cart 

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    #This __iter__() method will allow you to easily iterate over the items in the cart in views and templates.
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart =self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity'] #iterate over the cart items,converting each item's price back into decimal, and adding a total_price attribute to each item
            yield item

# A custom __len__() method to return the total number of items stored in the cart

    def __len__(self):
        return sum(itemz['quantity'] for item in self.cart.values())

# A method to calculate the total cost of the items in the cart

    def get_total_price(self):
        return sum(Decimal(item['price']) * item ['quantity'] for item in self.cart.values ())


# A method to clear the cart session

    def clear(self):
        del self.session [settings.CART_SESSION_ID]
        self.save()
        



#You use the product ID as a key in the cart's content dictionary. 
# You convert the product ID into a string because Django uses JSON to serialize session data, 
# and JSON only allows string key names. The product ID is the key, and the value
# that you persist is a dictionary with quantity and price figures for the product.
# The product's price is converted from decimal into a string in order to serialize it.
#  Finally, you call the save() method to save the cart in the session.


