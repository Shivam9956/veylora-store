# E-Commerce Store — Development Rules

## 1. General Rules
1. Build the MVP first.
2. Do not add unnecessary features.
3. Follow the PRD as the source of truth.
4. Do not change architecture without documenting the reason.
5. Keep code simple and readable.
6. Prefer Django built-in functionality where practical.

## 2. Backend Rules
- Use Python and Django.
- Use Django ORM.
- Use migrations for all database schema changes.
- Validate all user input server-side.
- Calculate prices and totals on the server.
- Never trust cart prices/total values from JavaScript.
- Use transactions for order creation.
- Do not allow checkout with insufficient stock.
- Do not allow negative stock.
- Use authentication decorators/mixins for protected pages.
- Do not expose sensitive information.

## 3. Frontend Rules
- Use HTML5, CSS3, and vanilla JavaScript.
- Do not use React/Vue/Angular.
- Avoid large UI libraries unless explicitly requested.
- Use semantic HTML.
- Responsive-first layout.
- Buttons must have clear states.
- Forms must show useful validation/error messages.
- Use accessible labels and meaningful alt text.
- Do not put business secrets in JavaScript.

## 4. UI/UX Rules
- Clean modern e-commerce interface.
- Consistent spacing, typography, cards, buttons, and forms.
- Mobile navigation must work.
- Product images must not break layout.
- Show loading/empty/error/success states.
- Cart count should update after cart changes.
- Avoid excessive animations.
- Maintain readable contrast.

## 5. Database Rules
- Use ForeignKey relationships correctly.
- Add indexes only where justified.
- Use DecimalField for money, never float.
- Use slugs for product/category URLs.
- Keep historical order snapshots.
- Use nullable product relation in OrderItem when appropriate so old orders survive product deletion.

## 6. Authentication Rules
- Use Django's password hashing.
- Never store passwords manually.
- Protect checkout and order history.
- Users may only see their own orders.
- Admin functionality belongs behind Django admin permissions.

## 7. Git Rules
Recommended commits:
- feat: initialize django project
- feat: add product catalog
- feat: add product detail
- feat: add session cart
- feat: add authentication
- feat: add checkout
- feat: add order processing
- feat: add admin
- test: add ecommerce tests
- fix: resolve checkout stock validation

Do not commit:
- .env
- database dumps containing sensitive data
- secrets
- unnecessary build/cache files

## 8. Error Handling
Every important operation needs:
- validation
- graceful failure
- user-friendly message
- server-side logging where appropriate

Never expose Python tracebacks to end users in production.

## 9. Code Quality
- Small functions
- Meaningful names
- Avoid duplicated logic
- Comments only when they explain why
- Keep templates readable
- Keep business logic out of JavaScript when server validation is required

## 10. Anti-Overengineering Rule
Do not implement payment gateways, APIs, Redis, Celery, Docker, microservices, or advanced frontend frameworks unless a task explicitly requires them.
