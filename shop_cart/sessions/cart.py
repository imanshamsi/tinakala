from django.conf import settings
from decimal import Decimal

from shop_products.models import Product


class Cart(object):

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, product_count=1, update_count=False):

        product_code = str(product.code)
        if product_code not in self.cart:
            self.cart[product_code] = {'product_count': 0,
                                       'price': str(product.price), }

        if update_count:
            self.cart[product_code]['product_count'] = product_count
        else:
            self.cart[product_code]['product_count'] += product_count
        self.cart[product_code]['price'] = str(product.price)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_code = str(product.code)
        if product_code in self.cart:
            del self.cart[product_code]
            self.save()

    def __iter__(self):
        product_codes = self.cart.keys()
        products = Product.objects.filter(code__in=product_codes)
        for product in products:
            self.cart[str(product.code)]['product'] = product
            self.cart[str(product.code)]['price'] = str(product.price)

            inventory = product.inventory
            demand = self.cart[str(product.code)]['product_count']
            if demand > inventory:
                self.cart[str(product.code)]['product_count'] = inventory

            if not product.status:
                del self.cart[product.code]

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['product_count']
            item['nice_price'] = f'{item["price"]:,}'
            item['nice_total_price'] = f'{item["total_price"]:,}'
            yield item

    def __len__(self):
        return sum(item['product_count'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['product_count'] for item in self.cart.values())

    def get_nice_total_price(self):
        return f'{self.get_total_price():,}'

    def get_point_shop(self):
        return round(self.get_total_price()/200000)

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
