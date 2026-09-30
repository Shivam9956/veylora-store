from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds sample categories and products for testing and demonstration.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial categories and products...')

        categories_data = [
            {'name': 'Electronics', 'description': 'High-performance gadgets, devices, and productivity tools.'},
            {'name': 'Audio & Sound', 'description': 'Premium headphones, wireless earphones, and studio speakers.'},
            {'name': 'Apparel & Fashion', 'description': 'Timeless everyday essentials crafted from durable materials.'},
            {'name': 'Home & Living', 'description': 'Modern workspace accessories and minimalist home goods.'},
        ]

        categories_map = {}
        for cat_info in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_info['name'],
                defaults={'description': cat_info['description']}
            )
            categories_map[cat.name] = cat
            status_text = 'Created' if created else 'Existing'
            self.stdout.write(f"Category: {cat.name} ({status_text})")

        products_data = [
            {
                'category': 'Audio & Sound',
                'name': 'Wireless Noise-Cancelling Headphones Pro',
                'description': 'Experience studio-grade acoustics with advanced active noise cancellation, 40-hour battery life, and ultra-plush memory foam ear cushions.',
                'price': Decimal('199.99'),
                'old_price': Decimal('249.99'),
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700&auto=format&fit=crop&q=80',
                'stock': 25,
            },
            {
                'category': 'Audio & Sound',
                'name': 'Portable Waterproof Bluetooth Speaker',
                'description': '360-degree immersive sound with deep bass, IPX7 waterproof rating, and up to 20 hours of continuous playtime.',
                'price': Decimal('79.99'),
                'old_price': Decimal('99.99'),
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=700&auto=format&fit=crop&q=80',
                'stock': 40,
            },
            {
                'category': 'Electronics',
                'name': 'Ergonomic Mechanical Keyboard RGB',
                'description': 'Custom tactile mechanical switches, aircraft-grade aluminum frame, hot-swappable PCB, and programmable per-key RGB backlighting.',
                'price': Decimal('129.50'),
                'old_price': Decimal('159.00'),
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=700&auto=format&fit=crop&q=80',
                'stock': 18,
            },
            {
                'category': 'Electronics',
                'name': 'Ultra-Fast Magnetic Wireless Charger Pad',
                'description': 'Sleek 15W Qi-certified rapid charging pad compatible with all modern smartphones and wireless earbuds.',
                'price': Decimal('34.99'),
                'old_price': Decimal('45.00'),
                'image_url': 'https://images.unsplash.com/photo-1622445262464-84b1456045b6?w=700&auto=format&fit=crop&q=80',
                'stock': 50,
            },
            {
                'category': 'Electronics',
                'name': '4K Ultra-HD Webcam with Dual Mics',
                'description': 'Crisp 60fps streaming webcam featuring AI autofocus, automatic low-light correction, and built-in privacy shutter.',
                'price': Decimal('89.00'),
                'old_price': None,
                'image_url': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=700&auto=format&fit=crop&q=80',
                'stock': 12,
            },
            {
                'category': 'Home & Living',
                'name': 'Solid Walnut Wood Monitor Stand',
                'description': 'Handcrafted premium American walnut desk riser with integrated cable management slot and brushed steel legs.',
                'price': Decimal('68.00'),
                'old_price': Decimal('85.00'),
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=700&auto=format&fit=crop&q=80',
                'stock': 15,
            },
            {
                'category': 'Home & Living',
                'name': 'Minimalist Ceramic Coffee Dripper & Carafe',
                'description': 'Heat-resistant borosilicate glass carafe paired with an artisanal matte ceramic dripper for the perfect pour-over brew.',
                'price': Decimal('42.00'),
                'old_price': None,
                'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=700&auto=format&fit=crop&q=80',
                'stock': 30,
            },
            {
                'category': 'Apparel & Fashion',
                'name': 'Water-Resistant Commuter Backpack 24L',
                'description': 'Engineered with weatherproof 900D ballistic nylon, padded 16-inch laptop compartment, and ergonomic airflow back panel.',
                'price': Decimal('115.00'),
                'old_price': Decimal('140.00'),
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700&auto=format&fit=crop&q=80',
                'stock': 20,
            },
            {
                'category': 'Apparel & Fashion',
                'name': 'Heavyweight Organic Cotton Everyday Hoodie',
                'description': 'Pre-shrunk 450 GSM French terry cotton with relaxed tailored fit, double-lined hood, and reinforced ribbing.',
                'price': Decimal('75.00'),
                'old_price': None,
                'image_url': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=700&auto=format&fit=crop&q=80',
                'stock': 35,
            },
        ]

        for p_data in products_data:
            cat = categories_map[p_data['category']]
            prod, created = Product.objects.get_or_create(
                name=p_data['name'],
                category=cat,
                defaults={
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'old_price': p_data['old_price'],
                    'image_url': p_data.get('image_url'),
                    'stock': p_data['stock'],
                    'is_active': True,
                }
            )
            # Update image_url if not set
            if not prod.image and p_data.get('image_url') and prod.image_url != p_data.get('image_url'):
                prod.image_url = p_data.get('image_url')
                prod.save(update_fields=['image_url'])

            status_text = 'Created' if created else 'Updated'
            self.stdout.write(f"Product: {prod.name} - ${prod.price} ({status_text})")

        # Create or update default Superuser for Admin dashboard
        from django.contrib.auth.models import User
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        admin_status = 'Created' if admin_created else 'Password synchronized'
        self.stdout.write(f"Superuser 'admin' ({admin_status}) - login with 'admin' / 'admin123'")

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample categories, products, and admin superuser!'))
