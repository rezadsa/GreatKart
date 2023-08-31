from carts.models import CartItem

def cartLength(request):
    if 'admin' in request.path:
        return dict(cart_length='Admin')
    length=0
    try:
        cartItems=CartItem.objects.filter(cart__cart_id=request.session.session_key).all()
        for item in cartItems:
            length += item.quantity
    except CartItem.DoesNotExist:
        pass
    
    return dict(cart_length=length)