from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from store.models import Product,Variation
from carts.models import Cart,CartItem

# Create your views here.

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    product_variation=[]
    if request.method == 'POST':
          for item in request.POST:
              key=item
              value=request.POST[key] 

              try:
                   variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                   product_variation.append(variation)
              except:
                   pass
                

    
    cart=None
    try:
        cart=Cart.objects.get(cart_id=request.session.session_key)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=request.session.session_key)
        cart.save()
    
    is_cartItem_exists=CartItem.objects.filter(cart=cart,product=product).exists()
    updated_item=False
    if is_cartItem_exists:
        cartItem=CartItem.objects.filter(cart=cart,product=product)
        ex_var_list=[]
        for item in cartItem:
             ex_var_list.append(list(item.variation.all()))
        
             if product_variation in ex_var_list:
                  quantity=item.quantity
                  item.quantity=quantity+1 if quantity<item.product.stock else quantity
                  item.save()
                  updated_item=True
                  break
             
             
        
    if not is_cartItem_exists or (is_cartItem_exists and not updated_item) :
      cartItem=CartItem.objects.create(product=product,cart=cart,quantity=1)
      if len(product_variation) > 0:
               for item in product_variation:
                    cartItem.variation.add(item)
      cartItem.save()

    return redirect('cart')

def increase_cart(request,cartItem_id):
     try:
          cart=Cart.objects.get(cart_id=request.session.session_key)
          cartItem=CartItem.objects.get(cart=cart,id=cartItem_id)
          if cartItem.quantity<cartItem.product.stock:
               cartItem.quantity+=1
               cartItem.save()
     except:
          None

     return redirect('cart')

def sub_cart(request,cartItem_id):
    
    try:
        cart=Cart.objects.get(cart_id=request.session.session_key)
        cartItem=CartItem.objects.get(cart=cart,id=cartItem_id)
        if cartItem.quantity>0:
            cartItem.quantity-=1
            cartItem.save()
    except cartItem.DoesNotExist or Cart.DoesNotExist:
         None

    return redirect('cart')

def remove_cartItem(request,cartItem_id):

     try:
          cart=Cart.objects.get(cart_id=request.session.session_key)
          CartItem.objects.get(cart=cart,id=cartItem_id).delete()
     except Cart.DoesNotExist or CartItem.DoesNotExist:
          None
        
     return redirect('cart')

def cart(request):
    TAX_RATE= 0.1
    total_amount=0
    tax=0
    total_payment=0
    try:
         cartItems=CartItem.objects.filter(cart__cart_id=request.session.session_key).all()
         for item in cartItems:
              total_amount+=item.quantity*item.product.price
         tax=float(total_amount)* TAX_RATE
         total_payment=float(total_amount)+tax
         
    except CartItem.DoesNotExist:
         cartItems=None
    
    context={
         'cartItems': cartItems,
         'total_amount': total_amount,
         'total_payment':total_payment,
         'tax': tax,
    }
    return render(request,'carts/cart.html',context)
