import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CustomerRegistrationForm, CustomerLoginForm, CheckoutForm, CustomerProfileForm


# ----------------------------------------------------------------------
# Product Catalog Views
# ----------------------------------------------------------------------

def home_view(request):
    """
    Home page view displaying hero banner, featured categories,
    and trending/featured products.
    """
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[8:16]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'latest_products': latest_products,
    }
    return render(request, 'store/home.html', context)


def product_list_view(request, category_slug=None):
    """
    Product listing view with search, category filtering,
    sorting, and pagination.
    """
    category = None
    categories = Category.objects.all()
    products_qs = Product.objects.filter(is_active=True)

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_qs = products_qs.filter(category=category)

    # Search keyword filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products_qs = products_qs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products_qs = products_qs.order_by('price')
    elif sort_by == 'price_high':
        products_qs = products_qs.order_by('-price')
    elif sort_by == 'name_asc':
        products_qs = products_qs.order_by('name')
    elif sort_by == 'name_desc':
        products_qs = products_qs.order_by('-name')
    else:  # 'newest'
        products_qs = products_qs.order_by('-created_at')

    # Pagination (12 items per page)
    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get('page')
    try:
        products = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        products = paginator.get_page(1)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_count': products_qs.count(),
    }
    return render(request, 'store/products.html', context)


def product_detail_view(request, slug):
    """
    Product detail view showing full details, stock status,
    quantity selector, and related products from same category.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


# ----------------------------------------------------------------------
# Shopping Cart Views
# ----------------------------------------------------------------------

def cart_detail_view(request):
    """
    Display current items in shopping cart, subtotal, shipping, and total.
    """
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)


@require_POST
def cart_add_view(request, product_id):
    """
    Add item to cart or increment quantity.
    Supports both traditional POST redirects and AJAX requests.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    override = request.POST.get('override') == 'True'

    if product.stock <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'This product is out of stock.'}, status=400)
        messages.error(request, f'"{product.name}" is currently out of stock.')
        return redirect('store:product_detail', slug=product.slug)

    added_qty = cart.add(product=product, quantity=quantity, override_quantity=override)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" added to cart.',
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_total': str(cart.get_total()),
            'item_quantity': added_qty,
        })

    messages.success(request, f'"{product.name}" added to your cart.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'store:cart_detail'
    return redirect(next_url)


@require_POST
def cart_update_view(request, product_id):
    """
    Update item quantity directly from the cart table.
    """
    cart = Cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    cart.update(product_id=product_id, quantity=quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_shipping': str(cart.get_shipping()),
            'cart_total': str(cart.get_total()),
        })

    messages.success(request, 'Cart updated successfully.')
    return redirect('store:cart_detail')


@require_POST
def cart_remove_view(request, product_id):
    """
    Remove an item from the cart.
    """
    cart = Cart(request)
    cart.remove_by_id(product_id)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_shipping': str(cart.get_shipping()),
            'cart_total': str(cart.get_total()),
        })

    messages.info(request, 'Item removed from cart.')
    return redirect('store:cart_detail')


@require_POST
def cart_clear_view(request):
    """
    Clear entire cart.
    """
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Your cart has been cleared.')
    return redirect('store:cart_detail')


# ----------------------------------------------------------------------
# Authentication Views
# ----------------------------------------------------------------------

def register_view(request):
    """
    User registration view. Automatically logs the user in upon successful sign-up.
    """
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to E-Commerce Store, {user.first_name or user.username}!')
            next_url = request.GET.get('next') or 'store:home'
            return redirect(next_url)
        else:
            messages.error(request, 'Please correct the errors below to register.')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'store/auth/register.html', {'form': form})


def login_view(request):
    """
    User login view with next redirect support.
    """
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or 'store:home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = CustomerLoginForm()

    next_url = request.GET.get('next', '')
    return render(request, 'store/auth/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """
    Log out the active user.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('store:home')


@login_required
def account_view(request):
    """
    Customer account dashboard showing profile info and recent orders.
    """
    user = request.user
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('store:account')
    else:
        form = CustomerProfileForm(instance=user)

    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]

    context = {
        'form': form,
        'recent_orders': recent_orders,
    }
    return render(request, 'store/auth/account.html', context)


# ----------------------------------------------------------------------
# Checkout & Order Views
# ----------------------------------------------------------------------

@login_required
def checkout_view(request):
    """
    Checkout view: validates cart, locks stock, creates transactional order and order items,
    decrements inventory, clears session cart, and redirects to success.
    """
    cart = Cart(request)

    if cart.is_empty():
        messages.warning(request, 'Your cart is empty. Please add products before checking out.')
        return redirect('store:product_list')

    # Initial stock availability check
    for item in cart:
        if item['quantity'] > item['product'].stock:
            messages.error(
                request,
                f'Insufficient stock for "{item["product"].name}". Only {item["product"].stock} available.'
            )
            return redirect('store:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Re-query products with select_for_update to lock rows and prevent race conditions
                    cart_items_data = []
                    subtotal = Decimal('0.00')

                    for item in cart:
                        # Lock product row in database
                        product = Product.objects.select_for_update().get(id=item['product'].id)
                        req_qty = item['quantity']

                        if product.stock < req_qty:
                            raise ValueError(
                                f'Stock changed! Only {product.stock} units of "{product.name}" are available now.'
                            )

                        item_subtotal = product.price * req_qty
                        subtotal += item_subtotal

                        cart_items_data.append({
                            'product': product,
                            'name_snapshot': product.name,
                            'price_snapshot': product.price,
                            'quantity': req_qty,
                            'subtotal': item_subtotal,
                        })

                    # Calculate shipping and grand total server-side
                    shipping = Decimal('0.00') if subtotal >= Decimal('100.00') else Decimal('10.00')
                    grand_total = subtotal + shipping

                    # Create Order
                    order = Order.objects.create(
                        user=request.user,
                        full_name=form.cleaned_data['full_name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        pincode=form.cleaned_data['pincode'],
                        subtotal=subtotal,
                        shipping=shipping,
                        total=grand_total,
                        status=Order.StatusChoices.CONFIRMED
                    )

                    # Create OrderItems and safely decrement inventory
                    for item_data in cart_items_data:
                        OrderItem.objects.create(
                            order=order,
                            product=item_data['product'],
                            product_name_snapshot=item_data['name_snapshot'],
                            price_snapshot=item_data['price_snapshot'],
                            quantity=item_data['quantity'],
                            subtotal=item_data['subtotal']
                        )

                        # Decrement stock
                        item_data['product'].stock -= item_data['quantity']
                        item_data['product'].save()

                    # Clear session cart after successful order creation
                    cart.clear()

                    messages.success(request, f'Order placed successfully! Order #{order.order_number}')
                    return redirect('store:order_success', order_number=order.order_number)

            except ValueError as e:
                messages.error(request, str(e))
                return redirect('store:cart_detail')
            except Exception as e:
                messages.error(request, 'An error occurred while placing your order. Please try again.')
                return redirect('store:checkout')
        else:
            messages.error(request, 'Please fix the errors in the shipping form.')
    else:
        # Pre-fill checkout form with user information if available
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'subtotal': cart.get_subtotal(),
        'shipping': cart.get_shipping(),
        'total': cart.get_total(),
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success_view(request, order_number):
    """
    Order confirmation view with full order overview and receipt details.
    """
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'store/order_success.html', context)


@login_required
def order_list_view(request):
    """
    Customer order history view.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'store/orders.html', context)


@login_required
def order_detail_view(request, order_number):
    """
    Customer detailed order receipt view with snapshot data.
    """
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)
