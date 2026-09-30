from .cart import Cart
from .models import Category


def store_context(request):
    """
    Context processor to supply cart and active categories to all templates safely.
    """
    try:
        cart = Cart(request)
    except Exception:
        cart = None

    try:
        nav_categories = list(Category.objects.all()[:8])
    except Exception:
        nav_categories = []

    return {
        'cart': cart,
        'nav_categories': nav_categories,
    }

