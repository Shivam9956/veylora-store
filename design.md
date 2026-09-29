# E-Commerce Store — UI/UX Design Specification

## 1. Design Direction
Style: modern, clean, professional, minimal e-commerce.

Target impression:
- trustworthy
- easy to browse
- fast
- product-focused
- mobile-friendly

## 2. Suggested Visual System
Use CSS variables so the theme can be changed easily.

Example:
--primary: #2563eb;
--primary-dark: #1d4ed8;
--text: #111827;
--muted: #6b7280;
--background: #f8fafc;
--surface: #ffffff;
--border: #e5e7eb;
--success: #16a34a;
--danger: #dc2626;

These are starting values, not mandatory. Maintain consistent contrast.

## 3. Typography
Use a clean sans-serif font.
Suggested:
- Inter
- system-ui
- Arial fallback

Headings:
- strong hierarchy
- short lines
- responsive font sizes

## 4. Global Layout
Header:
- Logo/store name
- Home
- Products
- Cart with item count
- Login/Account

Main:
- max-width container
- responsive gutters

Footer:
- Store description
- Quick links
- Contact placeholder
- Copyright

## 5. Home Page
Order:
1. Header
2. Hero section
3. Featured products
4. Categories
5. Why shop with us
6. CTA
7. Footer

Hero:
- clear headline
- short supporting text
- Shop Now button
- optional visual/product image

## 6. Product Cards
Card contains:
- image
- category
- name
- short description
- price
- old price if available
- stock indicator
- View Details
- Add to Cart

Hover:
- subtle elevation
- no excessive animation

## 7. Product Details
Desktop:
Two-column layout:
left = image
right = information

Mobile:
single column

Controls:
- quantity stepper
- Add to Cart
- stock status

## 8. Cart Page
Desktop:
- item list on left
- summary on right

Mobile:
- stacked layout

Cart summary:
- subtotal
- shipping
- total
- checkout button

## 9. Checkout
Use a clear two-column desktop layout:
left = customer/shipping form
right = order summary

Mobile:
form first, summary second.

## 10. Authentication Pages
Centered card:
- logo/name
- heading
- fields
- primary CTA
- link to alternate auth page
- validation messages

## 11. Order Success
Show:
- success message
- order number
- total
- View Order
- Continue Shopping

## 12. Order History
Table/card:
- order number
- date
- status
- total
- View Details

Mobile can use cards instead of wide tables.

## 13. Responsive Breakpoints
Suggested:
- mobile: < 640px
- tablet: 640–1024px
- desktop: > 1024px

Do not rely on fixed widths that cause horizontal scrolling.

## 14. UX States
Every page should consider:
- loading
- empty
- success
- validation error
- server error
- out-of-stock

## 15. Accessibility
- semantic headings
- label every form input
- visible focus state
- keyboard-accessible controls
- alt text for meaningful images
- sufficient contrast
- do not rely only on color for status
