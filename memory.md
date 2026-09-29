# E-Commerce Store — Project Memory

## Project Identity
Name: Basic E-Commerce Store
Purpose: Full-stack learning/project application demonstrating catalog, cart, authentication, checkout, and order management.

## Technology Decisions
Frontend:
- HTML
- CSS
- Vanilla JavaScript

Backend:
- Python
- Django

Database:
- SQLite during development
- PostgreSQL-ready for production

Authentication:
- Django built-in authentication

Admin:
- Django Admin

## Product Scope
MVP includes:
- Home
- Product listing
- Product details
- Search/filter/sort
- Cart
- Registration/login/logout
- Checkout
- Order processing
- Order history
- Admin product/order management

## Important Business Rules
1. Browser data is never trusted for prices.
2. Server calculates order totals.
3. Stock is checked during add-to-cart and again during checkout.
4. Order creation is transactional.
5. Historical order item name/price are stored as snapshots.
6. Customers can only view their own orders.
7. Admin manages catalog and order status.
8. Passwords are handled only by Django authentication.

## Current Architecture
Django monolith with server-rendered HTML and vanilla JavaScript enhancement.

## Future Ideas — Do Not Build Yet
- Razorpay/Stripe/PayPal
- Coupons
- Wishlist
- Reviews
- Product ratings
- Email notifications
- SMS/WhatsApp notifications
- Advanced analytics
- Redis
- Celery
- DRF API
- React frontend
- PostgreSQL deployment

## Antigravity Working Instructions
Before coding:
1. Read prd.md
2. Read architecture.md
3. Read rules.md
4. Read design.md
5. Read tasks.md
6. Use this file as persistent project context

During implementation:
- Complete tasks in order.
- Keep changes small and testable.
- Update tasks.md when a task is completed.
- Do not silently change requirements.
- If a requirement conflicts with an existing implementation, prioritize the PRD and document the change.
- Run tests after major backend changes.
- Do not mark incomplete features as complete.

## Final Verification Flow
Admin creates product
→ customer registers
→ customer logs in
→ customer browses
→ customer views details
→ customer adds item
→ customer updates cart
→ customer checks out
→ order is created
→ stock decreases
→ cart clears
→ order confirmation appears
→ order appears in customer history
→ admin can view/update order.
