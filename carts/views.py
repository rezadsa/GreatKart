from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from store.models import Product,Variation
from carts.models import Cart,CartItem
from django.contrib.auth.decorators import login_required


# Create your views here.

def _cart_id(request):
     cart=request.session.session_key 
     if not cart:
          request.session.create()
          cart=request.session.session_key

     return cart

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
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
    if request.user.is_authenticated:
         is_cartItem_exists=CartItem.objects.filter(user=request.user,product=product).exists()
    else:
        is_cartItem_exists=CartItem.objects.filter(cart=cart,product=product).exists()

    updated_item=False
    if is_cartItem_exists:
            
        if request.user.is_authenticated:
               cartItem=CartItem.objects.filter(user=request.user,product=product)
        else:
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
      if request.user.is_authenticated:
          cartItem=CartItem.objects.create(product=product,user=request.user,quantity=1)
      else:      
           cartItem=CartItem.objects.create(product=product,cart=cart,quantity=1)

      if len(product_variation) > 0:
               for item in product_variation:
                    cartItem.variation.add(item)
      cartItem.save()

    return redirect('cart')

def increase_cart(request,cartItem_id):
     try:
          if request.user.is_authenticated:
               cartItem=CartItem.objects.get(user=request.user,id=cartItem_id)
          else:
               cart=Cart.objects.get(cart_id=_cart_id(request))
               cartItem=CartItem.objects.get(cart=cart,id=cartItem_id)
          if cartItem.quantity<cartItem.product.stock:
               cartItem.quantity+=1
               cartItem.save()
     except:
          None

     return redirect('cart')

def sub_cart(request,cartItem_id):
    
    try:
        if request.user.is_authenticated:
          cartItem=CartItem.objects.get(user=request.user,id=cartItem_id)
        else:  
          cart=Cart.objects.get(cart_id=_cart_id(request))
          cartItem=CartItem.objects.get(cart=cart,id=cartItem_id)

        if cartItem.quantity>0:
            cartItem.quantity-=1
            cartItem.save()
    except cartItem.DoesNotExist or Cart.DoesNotExist:
         None

    return redirect('cart')

def remove_cartItem(request,cartItem_id):

     try:
          if request.user.is_authenticated:
               CartItem.objects.get(user=request.user,id=cartItem_id).delete()
          else:
               cart=Cart.objects.get(cart_id=_cart_id(request))
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
         if request.user.is_authenticated:
               cartItems=CartItem.objects.filter(user=request.user,is_active=True).all()
         else:
               cartItems=CartItem.objects.filter(cart__cart_id=_cart_id(request),is_active=True).all()

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

@login_required(login_url='login')
def checkout(request):

    TAX_RATE= 0.1
    total_amount=0
    tax=0
    total_payment=0
    try:
         cartItems=CartItem.objects.filter(user=request.user).all()
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


    return render(request,'carts/checkout.html',context)
