from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Catalog
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list_view, name='product_list_by_category'),
    path('products/<slug:slug>/', views.product_detail_view, name='product_detail'),

    # Shopping Cart
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update_view, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove_view, name='cart_remove'),
    path('cart/clear/', views.cart_clear_view, name='cart_clear'),

    # Authentication & Account
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),

    # Checkout & Orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('orders/', views.order_list_view, name='orders'),
    path('orders/<str:order_number>/', views.order_detail_view, name='order_detail'),
]
