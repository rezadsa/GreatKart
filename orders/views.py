from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from .forms import OrderForm
from .models import Order 

from greatkart.settings import TAX_RATE

import datetime

# Create your views here.

@login_required(login_url='login')
def payment(request):
        
    current_user=request.user

    cartItems=CartItem.objects.filter(user=current_user)
    if cartItems.count()<=0:
        return redirect('store')
    
    grand_total=0
    for item in cartItems:
        grand_total+=item.product.price*item.quantity
    
    tax=float(grand_total)*float(TAX_RATE)
    
    order_already_exists=Order.objects.filter(user=current_user,status='New',is_ordered=False).exists()
    if order_already_exists:
             order=Order.objects.get(user=current_user,status='New',is_ordered=False)
    else:
            if request.method == 'POST':
                form =OrderForm(request.POST)
                if not form.is_valid():  
                     return redirect('/cart/checkout')
                else:      

                    data=Order()
                    
                    data.first_name     =form.cleaned_data['first_name']
                    data.last_name      =form.cleaned_data['last_name']
                    data.email          =form.cleaned_data['email']
                    data.phone          =form.cleaned_data['phone']
                    data.address_line_1 =form.cleaned_data['address_line_1']
                    data.address_line_2 =form.cleaned_data['address_line_2']
                    data.postcode       =form.cleaned_data['postcode']
                    data.city           =form.cleaned_data['city']
                    data.country        =form.cleaned_data['country']
                    data.order_note     =form.cleaned_data['order_note']

                    data.order_total   =grand_total 

                    data.tax           =tax

                    data.user=current_user

                    data.ip=request.META.get('REMOTE_ADDR')
                    data.save()

                    #Generate order number
                    yr=int(datetime.date.today().strftime('%Y'))
                    dt=int(datetime.date.today().strftime('%d'))
                    mt=int(datetime.date.today().strftime('%m'))

                    d=datetime.date(yr,mt,dt)
                    current_date=d.strftime('%Y%m%d')

                    order_number=current_date+str(data.id)

                    data.order_number=order_number

                    data.save()

                    order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)

    context={
        'order': order,
        'cartItems': cartItems,
        'total_amount': grand_total,
        'total_payment':float(grand_total)+float(tax),
        'tax': tax,
    }

    return render(request,'orders/payment.html',context)

def deleteOrder(request,order_number):
     Order.objects.get(order_number=order_number).delete()
     return redirect('checkout')
     
       
           

 
    
