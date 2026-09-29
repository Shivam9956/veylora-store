# E-Commerce Store — Architecture

## 1. Architecture Choice
Use a Django monolithic architecture for the MVP.

Browser
  ↓
HTML/CSS/Vanilla JS
  ↓
Django URLs / Views
  ↓
Django Models + Business Logic
  ↓
Database

Django Admin
  ↓
Models
  ↓
Database

## 2. Recommended Project Structure

ecommerce_store/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── store/
│   ├── migrations/
│   ├── templates/store/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── products.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_success.html
│   │   ├── orders.html
│   │   ├── order_detail.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── register.html
│   ├── static/store/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── cart.py
│   └── tests.py
└── media/
    └── products/

## 3. Application Responsibilities
### config
Global settings, root URL configuration, ASGI/WSGI.

### store
All e-commerce domain functionality:
- catalog
- cart
- authentication-related forms/views
- checkout
- orders
- admin configuration
- tests

## 4. Request Flow

### Product Listing
GET /products/
→ view queries active products
→ optional search/filter/sort
→ template renders cards

### Product Details
GET /products/<slug>/
→ fetch active product
→ render details

### Add to Cart
POST /cart/add/
→ validate product and quantity
→ validate stock
→ update session cart
→ return redirect or JSON response

### Checkout
GET /checkout/
→ require authentication
→ show cart and checkout form

POST /checkout/
→ validate user input
→ validate cart and stock
→ database transaction
→ create Order
→ create OrderItems
→ decrement stock
→ clear cart
→ redirect to success page

## 5. Cart Strategy
Use Django session for MVP.
Session structure concept:

cart = {
  "product_id": {
    "quantity": 2
  }
}

Never trust prices sent by the browser. Always retrieve current prices from the database on the server.

## 6. Order Integrity
Order creation must use a database transaction.

Pseudo-flow:
transaction.atomic()
  validate cart
  lock/recheck relevant stock where appropriate
  create order
  create order items
  decrement stock
  clear cart

If any step fails, rollback the complete order operation.

## 7. Security Architecture
- Django CSRF middleware
- Django password hashing
- LoginRequiredMixin/@login_required
- Server-side validation
- Escape template output
- No raw SQL unless necessary
- SECRET_KEY from environment in production
- DEBUG=false in production
- ALLOWED_HOSTS configured
- Secure cookies/HTTPS settings for production
- Never commit .env

## 8. Database
Development: SQLite.
Production-ready: PostgreSQL.

Use Django migrations for schema changes.

## 9. Static/Media
Static:
store/static/

Media:
media/products/

Development may use Django static serving. Production should use a proper static/media strategy.

## 10. Testing Layers
- Model tests
- Cart tests
- Authentication tests
- Checkout tests
- Order creation tests
- Stock validation tests
- Permission tests
- Basic page response tests

Critical test:
Two checkout attempts must not allow stock to become negative.

## 11. Future Scaling
If the project grows:
- Django REST Framework API
- PostgreSQL
- Redis/cache
- Celery background jobs
- Object storage/CDN for media
- Payment provider
- Email service
- Separate frontend if needed

Do not add these now unless required.
