from carts.models import CartItem
from .views import _cart_id


def cartLength(request):
    if 'admin' in request.path:
        return dict(cart_length='Admin')
    
    length=0
    try:
        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)
        else:
            cartItems=CartItem.objects.filter(cart__cart_id=_cart_id(request)).all()
        for item in cartItems:
            length += item.quantity
    except CartItem.DoesNotExist:
        pass
    
    return dict(cart_length=length)