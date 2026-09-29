from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product, Order, OrderItem
from store.cart import Cart, CART_SESSION_KEY


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.category = Category.objects.create(
            name='Electronics',
            description='Gadgets and devices'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Wireless Headphones',
            description='High quality sound',
            price=Decimal('99.99'),
            old_price=Decimal('129.99'),
            stock=15,
            is_active=True
        )

    def test_category_slug_auto_generation(self):
        self.assertEqual(self.category.slug, 'electronics')
        cat2 = Category.objects.create(name='Home & Kitchen')
        self.assertEqual(cat2.slug, 'home-kitchen')

    def test_product_slug_and_discount_properties(self):
        self.assertEqual(self.product.slug, 'wireless-headphones')
        self.assertTrue(self.product.is_in_stock)
        self.assertTrue(self.product.has_discount)
        self.assertEqual(self.product.discount_percent, 23)

        # Test duplicate product name slug collision handling
        prod2 = Product.objects.create(
            category=self.category,
            name='Wireless Headphones',
            description='Another version',
            price=Decimal('119.99'),
            stock=5
        )
        self.assertEqual(prod2.slug, 'wireless-headphones-1')

    def test_order_creation_and_snapshots(self):
        order = Order.objects.create(
            user=self.user,
            full_name='John Doe',
            email='john@example.com',
            phone='+1234567890',
            address='123 Main St',
            city='Tech City',
            state='State',
            pincode='12345',
            subtotal=Decimal('199.98'),
            shipping=Decimal('10.00'),
            total=Decimal('209.98'),
            status=Order.StatusChoices.PENDING
        )
        self.assertTrue(order.order_number.startswith('ORD-'))
        self.assertEqual(order.status, 'PENDING')

        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name_snapshot=self.product.name,
            price_snapshot=self.product.price,
            quantity=2
        )
        self.assertEqual(item.subtotal, Decimal('199.98'))
        self.assertEqual(str(item), '2 x Wireless Headphones')

    def test_order_item_survives_product_deletion(self):
        order = Order.objects.create(
            user=self.user,
            full_name='Jane Doe',
            email='jane@example.com',
            phone='+1234567890',
            address='456 Elm St',
            city='Tech City',
            state='State',
            pincode='12345',
            subtotal=Decimal('99.99'),
            shipping=Decimal('0.00'),
            total=Decimal('99.99')
        )
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name_snapshot=self.product.name,
            price_snapshot=self.product.price,
            quantity=1
        )
        self.product.delete()
        item.refresh_from_db()
        self.assertIsNone(item.product)
        self.assertEqual(item.product_name_snapshot, 'Wireless Headphones')
        self.assertEqual(item.price_snapshot, Decimal('99.99'))


class CatalogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Laptops')
        self.product = Product.objects.create(
            category=self.category,
            name='Pro Ultrabook 14',
            description='Lightweight high performance laptop',
            price=Decimal('999.00'),
            stock=8,
            is_active=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pro Ultrabook 14')

    def test_product_list_page(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pro Ultrabook 14')

    def test_product_list_filter_by_category(self):
        response = self.client.get(reverse('store:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pro Ultrabook 14')

    def test_product_list_search(self):
        response = self.client.get(reverse('store:product_list') + '?q=Ultrabook')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pro Ultrabook 14')

        response_empty = self.client.get(reverse('store:product_list') + '?q=NonExistentProduct')
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, 'No Products Found')

    def test_product_detail_page(self):
        response = self.client.get(reverse('store:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pro Ultrabook 14')
        self.assertContains(response, '$999.00')

    def test_product_detail_404_for_invalid_slug(self):
        response = self.client.get(reverse('store:product_detail', args=['non-existent-product']))
        self.assertEqual(response.status_code, 404)


class CartAndCheckoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='shopper',
            email='shopper@example.com',
            password='password123'
        )
        self.category = Category.objects.create(name='Accessories')
        self.product = Product.objects.create(
            category=self.category,
            name='USB-C Hub',
            description='Multiport adapter',
            price=Decimal('49.99'),
            stock=5,
            is_active=True
        )

    def test_cart_add_and_update(self):
        # Add to cart
        response = self.client.post(reverse('store:cart_add', args=[self.product.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 302)

        # Verify cart session
        session = self.client.session
        cart_data = session.get(CART_SESSION_KEY)
        self.assertIsNotNone(cart_data)
        self.assertEqual(cart_data[str(self.product.id)]['quantity'], 2)

        # Update cart quantity
        response = self.client.post(reverse('store:cart_update', args=[self.product.id]), {'quantity': 3})
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertEqual(session[CART_SESSION_KEY][str(self.product.id)]['quantity'], 3)

    def test_cart_remove_and_clear(self):
        self.client.post(reverse('store:cart_add', args=[self.product.id]), {'quantity': 2})
        self.client.post(reverse('store:cart_remove', args=[self.product.id]))
        session = self.client.session
        self.assertNotIn(str(self.product.id), session.get(CART_SESSION_KEY, {}))

    def test_cart_cannot_exceed_stock(self):
        # Request quantity 10 when stock is 5
        self.client.post(reverse('store:cart_add', args=[self.product.id]), {'quantity': 10})
        session = self.client.session
        # Clamped to available stock (5)
        self.assertEqual(session[CART_SESSION_KEY][str(self.product.id)]['quantity'], 5)

    def test_successful_checkout_and_stock_decrement(self):
        self.client.login(username='shopper', password='password123')
        # Add 2 items to cart
        self.client.post(reverse('store:cart_add', args=[self.product.id]), {'quantity': 2})

        checkout_data = {
            'full_name': 'Shopper Smith',
            'email': 'shopper@example.com',
            'phone': '+1 555-0199',
            'address': '789 Market Blvd',
            'city': 'San Francisco',
            'state': 'CA',
            'pincode': '94103',
            'order_notes': 'Please leave at front desk',
        }

        response = self.client.post(reverse('store:checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        # Verify order was created
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Shopper Smith')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product_name_snapshot, 'USB-C Hub')

        # Verify stock was decremented: 5 - 2 = 3
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # Verify cart was cleared
        session = self.client.session
        self.assertNotIn(CART_SESSION_KEY, session)

    def test_checkout_fails_if_stock_becomes_insufficient(self):
        self.client.login(username='shopper', password='password123')
        # Add 4 items to cart
        self.client.post(reverse('store:cart_add', args=[self.product.id]), {'quantity': 4})

        # Simultaneously reduce product stock to 2 in DB (e.g. concurrent checkout)
        self.product.stock = 2
        self.product.save()

        checkout_data = {
            'full_name': 'Shopper Smith',
            'email': 'shopper@example.com',
            'phone': '+1 555-0199',
            'address': '789 Market Blvd',
            'city': 'San Francisco',
            'state': 'CA',
            'pincode': '94103',
        }

        # Checkout attempt should fail and redirect to cart without decreasing stock below 0
        response = self.client.post(reverse('store:checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        # No order should have been created
        self.assertEqual(Order.objects.filter(user=self.user).count(), 0)
        # Stock should remain at 2 (not negative)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)


class AuthenticationAndSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass1234')
        self.order1 = Order.objects.create(
            user=self.user1,
            full_name='User One',
            email='user1@example.com',
            phone='123',
            address='Addr 1',
            city='City',
            state='State',
            pincode='123',
            subtotal=Decimal('50.00'),
            total=Decimal('60.00')
        )

    def test_user_registration(self):
        reg_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(reverse('store:register'), reg_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('store:checkout'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_user_cannot_access_other_users_order(self):
        self.client.login(username='user2', password='pass1234')
        # Attempt to access user1's order
        response = self.client.get(reverse('store:order_detail', args=[self.order1.order_number]))
        self.assertEqual(response.status_code, 404)
