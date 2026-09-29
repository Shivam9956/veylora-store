# E-Commerce Store — Product Requirements Document

## 1. Project Overview
Build a basic but production-structured e-commerce store using:
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Python + Django
- Database: SQLite for development, PostgreSQL-ready architecture for production
- Authentication: Django authentication system
- API/data exchange: Django JSON endpoints or Django REST Framework if needed

The application must be responsive, clean, easy to maintain, and organized so more features can be added later.

## 2. Primary Goal
Create an end-to-end shopping flow:
1. User visits store
2. Browses products
3. Opens product details
4. Adds products to cart
5. Reviews/updates cart
6. Registers/logs in
7. Proceeds to checkout
8. Places an order
9. Order is stored in the database
10. User can view order confirmation/history

## 3. User Roles
### Guest
- View home/product listing
- Search/filter products
- View product details
- Add items to cart
- View/update cart
- Register/login

### Customer
- All guest features
- Maintain account/session
- Checkout
- Place orders
- View order history
- View order details
- Logout

### Admin
Use Django Admin initially.
- Add/edit/delete products
- Manage categories
- Manage product stock
- View/update orders
- View users
- Manage order status

## 4. Core Features

### 4.1 Home Page
- Store logo/name
- Navigation: Home, Products, Cart, Login/Account
- Hero/banner section
- Featured products
- Category section
- Search
- Footer

### 4.2 Product Listing
Each product card should show:
- Product image
- Product name
- Short description
- Price
- Optional old price
- Stock status
- View Details
- Add to Cart

Support:
- Search by product name
- Filter by category
- Sort by price/name
- Pagination if product count becomes large

### 4.3 Product Details
Show:
- Large product image
- Product name
- Price
- Description
- Category
- Stock availability
- Quantity selector
- Add to Cart
- Related products

Prevent adding more quantity than available stock.

### 4.4 Shopping Cart
Cart must support:
- Add item
- Remove item
- Increase/decrease quantity
- Manual quantity update
- Subtotal
- Total quantity
- Grand total
- Empty-cart state
- Continue shopping
- Proceed to checkout

Cart should be persisted for logged-in users. Guest cart can use session storage/session-based cart.

### 4.5 Authentication
Use Django auth.
- Register
- Login
- Logout
- Password validation
- Protected checkout/order pages
- Account page
- Basic profile information

Never store plain-text passwords.

### 4.6 Checkout
Collect:
- Full name
- Email
- Phone
- Address
- City
- State
- Pincode
- Optional order notes

Show:
- Order items
- Quantity
- Product prices
- Subtotal
- Shipping
- Grand total

For MVP, payment method can be:
- Cash on Delivery / Demo Payment

Payment gateway should NOT be implemented unless explicitly requested later.

### 4.7 Order Processing
When order is placed:
- Validate cart
- Validate stock
- Create order
- Create order items
- Calculate totals server-side
- Reduce stock safely
- Clear cart
- Generate order number
- Show confirmation page

Order status:
- Pending
- Confirmed
- Processing
- Shipped
- Delivered
- Cancelled

### 4.8 Order History
Logged-in customer can:
- See previous orders
- Open order details
- See order number/date/status/total
- See item-level details

### 4.9 Admin
Django Admin should manage:
- Products
- Categories
- Orders
- Order items
- Users

Use useful list displays, filters, search, and readonly calculated fields where appropriate.

## 5. Data Model

### Category
- id
- name
- slug
- description
- created_at

### Product
- id
- category (FK)
- name
- slug
- description
- price
- old_price (nullable)
- image
- stock
- is_active
- created_at
- updated_at

### Order
- id
- order_number
- user (FK)
- full_name
- email
- phone
- address
- city
- state
- pincode
- subtotal
- shipping
- total
- status
- created_at
- updated_at

### OrderItem
- id
- order (FK)
- product (FK, nullable if product later deleted)
- product_name_snapshot
- price_snapshot
- quantity
- subtotal

The snapshot fields ensure historical orders remain understandable if a product changes later.

## 6. Non-Functional Requirements
- Responsive on mobile/tablet/desktop
- Semantic HTML
- Accessible labels and buttons
- Good keyboard usability
- Server-side validation
- CSRF protection
- Authentication authorization
- No secrets in source code
- Environment variables for sensitive settings
- Clear error states
- Loading states where AJAX/fetch is used
- Empty states
- 404/500 friendly pages
- Clean code and reusable components/templates
- Avoid unnecessary dependencies

## 7. Success Criteria
The project is complete when a new user can:
Register → Login → Browse → View product → Add to cart → Update cart → Checkout → Place order → See confirmation → See order history.

An admin can:
Login to Django Admin → Create category/product → Manage stock → View orders → Change order status.

## 8. Out of Scope for MVP
Do not implement unless later requested:
- Real payment gateway
- Coupons
- Reviews/ratings
- Wishlist
- Advanced recommendation engine
- Multi-vendor marketplace
- Delivery API
- Email/SMS automation
- Complex analytics
- Microservices
