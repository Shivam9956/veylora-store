from decimal import Decimal
from django.conf import settings
from .models import Product

CART_SESSION_KEY = 'ecommerce_cart'
SHIPPING_FLAT_RATE = Decimal('10.00')
FREE_SHIPPING_THRESHOLD = Decimal('100.00')


class Cart:
    """
    Session-based Shopping Cart.
    Stores only product IDs and quantities in session;
    retrieves real-time product prices directly from the database.
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        Validates against product available stock.
        """
        product_id = str(product.id)
        current_qty = self.cart.get(product_id, {}).get('quantity', 0)

        if override_quantity:
            new_qty = quantity
        else:
            new_qty = current_qty + quantity

        # Clamp to available stock
        if new_qty > product.stock:
            new_qty = product.stock

        if new_qty > 0:
            self.cart[product_id] = {'quantity': new_qty}
        else:
            self.remove(product)

        self.save()
        return new_qty

    def update(self, product_id, quantity):
        """
        Update the quantity of a specific item in the cart.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            try:
                product = Product.objects.get(id=int(product_id), is_active=True)
                qty = int(quantity)
                if qty <= 0:
                    self.remove_by_id(product_id)
                else:
                    self.cart[product_id]['quantity'] = min(qty, product.stock)
                    self.save()
            except (Product.DoesNotExist, ValueError):
                self.remove_by_id(product_id)

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        self.remove_by_id(str(product.id))

    def remove_by_id(self, product_id):
        """
        Remove a product by ID from the cart.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Clear all items from the cart.
        """
        if CART_SESSION_KEY in self.session:
            del self.session[CART_SESSION_KEY]
            self.session.modified = True

    def save(self):
        """
        Mark session as modified to ensure it is saved.
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart, populating product instances and calculating totals.
        """
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        products_map = {product.id: product for product in products}

        # Build clean list and purge any stale products
        stale_ids = []
        for product_id_str, item_data in list(self.cart.items()):
            product_id = int(product_id_str)
            product = products_map.get(product_id)
            if product is None:
                stale_ids.append(product_id_str)
                continue

            quantity = item_data.get('quantity', 1)
            if quantity <= 0:
                stale_ids.append(product_id_str)
                continue

            item = {
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total_price': product.price * quantity,
            }
            yield item

        for pid in stale_ids:
            if pid in self.cart:
                del self.cart[pid]
                self.save()

    def __len__(self):
        """
        Count total number of items in the cart.
        """
        return sum(item.get('quantity', 0) for item in self.cart.values())

    def get_subtotal(self):
        """
        Calculate total price of all items in cart based on live DB prices.
        """
        subtotal = Decimal('0.00')
        for item in self:
            subtotal += item['total_price']
        return subtotal

    def get_shipping(self):
        """
        Calculate shipping cost:
        - Free if subtotal exceeds FREE_SHIPPING_THRESHOLD or cart is empty
        - Flat rate otherwise
        """
        subtotal = self.get_subtotal()
        if subtotal == Decimal('0.00') or subtotal >= FREE_SHIPPING_THRESHOLD:
            return Decimal('0.00')
        return SHIPPING_FLAT_RATE

    def get_total(self):
        """
        Calculate grand total: subtotal + shipping.
        """
        return self.get_subtotal() + self.get_shipping()

    def is_empty(self):
        return len(self) == 0
