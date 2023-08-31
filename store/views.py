from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import Product
from category.models import Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from carts.models import CartItem
from django.db.models import Q



# Create your views here.

def store(request,category_slug=None):
  
    if category_slug:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True).order_by('-modified_date')
    else: 
        products=Product.objects.all().filter(is_available=True).order_by('-modified_date')

    product_count=products.count()

    paginator=Paginator(products,per_page=9)
    
    page=request.GET.get('page')

    try:
        page_object=paginator.get_page(page)   
    except PageNotAnInteger:
        page_object=paginator.get_page(1)
    except EmptyPage:
        page_object=paginator.get_page(paginator.num_pages)

        
    try:
        page=int(request.GET.get('page'))
    except :
        page=1
    page_object.elided=paginator.get_elided_page_range(number=page,on_each_side=3,on_ends=1)

    context={
        'paginator': page_object,
        'product_count': product_count,
        
    
    }

    return render(request,'store/store.html', context)

def product_detail(request,category_slug=None,product_slug=None):
    in_cart=False
    try:
        product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(product=product,cart__cart_id=request.session.session_key).exists()
    except Exception as e:
        raise e 

    context={
        'product':product,
        'in_cart':in_cart,
    }
   
    return render(request,'store/product_detail.html',context)

def search(request):
    page_object=None
    product_count=0
    if 'keyword' in request.GET:
        keyword=request.GET.get('keyword')
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(name__icontains=keyword))
            paginator=Paginator(products,per_page=9)

            page=request.GET.get('page')
            try:
                page=int(page)
            except:
                page=1

            if page>paginator.num_pages:
                page=paginator.num_pages


            page_object=paginator.get_page(page)

            page_object.elided=paginator.get_elided_page_range(page,on_each_side=3,on_ends=1)
            
            product_count=products.count()


  
    context={
        'paginator':page_object,
        'keyword':keyword,
        'product_count':product_count,
    }

    return render(request,'store/store.html',context)
