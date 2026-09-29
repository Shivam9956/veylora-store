from .cart import Cart
from .models import Category


def store_context(request):
    """
    Context processor to supply cart and active categories to all templates.
    """
    return {
        'cart': Cart(request),
        'nav_categories': Category.objects.all()[:8],
    }
