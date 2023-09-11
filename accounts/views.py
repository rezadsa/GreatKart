from django.shortcuts import render,redirect,HttpResponse
from .forms import RegisterForm
from .models import Account
from random import randint
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from carts.models import Cart,CartItem
from carts.views import _cart_id

import re
import requests

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.

     
def register(request):
    
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone=form.cleaned_data['phone']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            username=email.split('@')[0]
           
            while True:
                if Account.objects.filter(username=username).exists():
                    username=username+str(randint(0,9999))
                else:
                    break
              
           
            user=Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,   
                username=username,
                password=password
            )

            user.phone=phone
            user.save()

           
            current_site=get_current_site(request)
            mail_subject='Please actuvate your account.'
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                
                })

            to_email=user.email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            return redirect('/account/sendEmailMessage/?command=verification&email=%s' % to_email)

           
    else:
        form=RegisterForm()

    context={
                'form':form,
    }
    return render(request,'accounts/register.html',context)


def activate(request,uidb64,token):

    try:
        uidb64=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uidb64)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user and default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,'Congartulation! Your account is activated.')
            return redirect('login')
            
        
    else:
        messages.error(request,'Invalid Activation Link.')
        return redirect('register')


def forgotPassword(request):
     if request.method=='POST':
          email=request.POST.get('email')
          if Account.objects.filter(email__exact=email).exists():
               user=Account.objects.get(email__exact=email)

               subject='Great kart! reset password!'

               message=render_to_string('accounts/password_reset_verification.html',{
                    'user':user,
                    'token':default_token_generator.make_token(user),
                    'domain':get_current_site(request),
                    'uidb64':urlsafe_base64_encode(force_bytes(user.pk))

               })
               
               send_email=EmailMessage(subject,message,to=[user.email])
               send_email.send()
               return redirect('/account/sendEmailMessage/?command=resetpassword&email=%s' % user.email)
          else:
               messages.error(request,'Invalid reset password link.')
               return redirect('forgetPassword')
          
     return render(request,'accounts/forgot_password.html')

def resetpassword_validate(request,uidb64,token):
    try:
         uidb64 = urlsafe_base64_decode(uidb64).decode()
         user=Account.objects.get(pk=uidb64)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExists):
         user=None

    if user and default_token_generator.check_token(user,token):
         request.session['uid']=uidb64
         messages.success(request,'Please reset password.')
         return redirect('resetPassword')
    else:
        
         messages.error(request,'Invalid/expired reset password link.')
         return redirect('login')
        
def resetPassword(request):
     if request.method == 'POST':
          password=request.POST.get('password')
          confirmPassword=request.POST.get('confirm_password')
          error=False
          if password != confirmPassword:
               messages.error(request,'password must be matches.')
               error=True
          elif len(password) <8 :
               messages.error(request,'password must be at least 8 character.')
               error=True
          else:
               if not re.search('[a-z]',password):
                    messages.error(request,'password must has at least on lower case character.')
                    error=True
                    
               if not re.search('[A-Z]',password):
                    messages.error(request,'password must has at least on upper case character.')
                    error=True
               if not re.search('[0-9]',password):
                    messages.error(request,'password must has at least on digit[0-9].')
                    error=True
               if not re.search('[@!£$&*~#]',password):
                    messages.error(request,'password must has at least on especial character [@!£$&*~#].')
                    error=True
               

          if not error:
                uid=int(request.session.get('uid'))
                if Account.objects.filter(pk=uid).exists():
                    user=Account.objects.get(pk=uid)
                    user.set_password(password)
                    user.is_active=True
                    user.save()
                    messages.success(request,'password chenged successfully!!')
                    return redirect('login')
                                
                else:
                    messages.error(request,'Something went wrong, Please try agin.')
                    return redirect('forgotPassword')
          else:
                return redirect('resetPassword')
         
               
     return render(request,'accounts/resetPassword.html')
           
def login(request):

    if request.method == 'POST':
            email=request.POST.get('email')
            password=request.POST.get('password')

            user=auth.authenticate(email=email, password=password)
          
           
            if user :
               try:
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    if cart:
                         cartItem=CartItem.objects.filter(cart=cart)

                         product_variation=[]
                         pro_id=[]
                         for item in cartItem:
                              product_variation.append(list(item.variation.all()))
                              pro_id.append(item.id)

                         
                         ex_variation=[]
                         ex_id=[]
                         cartItem=CartItem.objects.filter(user=user)
                         for item in cartItem:
                              ex_variation.append(list(item.variation.all()))
                              ex_id.append(item.id)
                                                  
                         

                    for pr in product_variation:
                         if pr in ex_variation:
                              index=ex_variation.index(pr)
                              item_id=ex_id[index]
                              item=CartItem.objects.get(id=item_id)
                              item.quantity+=CartItem.objects.get(id=pro_id[product_variation.index(pr)]).quantity
                              
                              item.save()
                         else:
                              cartItem=CartItem.objects.filter(cart=cart)
                              for item in cartItem:
                                   item.user=user
                                   item.save()

               except:
                    pass

               auth.login(request, user)
               messages.success(request,f'{user.username}, Welcome. ')

               url=request.META.get('HTTP_REFERER')
              
               try:
                    query=requests.utils.urlparse(url).query
                    params=dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                         nextPage=params['next']
                         return redirect(nextPage)
                    
               except:
                    return redirect('dashboard')
                                     

            else:
                messages.error(request,'Username or Password is wrong!')
                return redirect('login')

   

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):

    auth.logout(request)
    messages.info(request,'You Logged out successfully.')


    return redirect('login')


     
def sendEmailMessage(request):
     
     return render(request,'accounts/send_email_message.html')

@login_required(login_url='login')
def dashboard(request):

    return render(request,'accounts/dashboard.html')

