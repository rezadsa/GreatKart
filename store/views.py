from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator


# Create your views here.

def store(request,category_slug=None):
    category=None
    product=None

    if category_slug:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
    else: 
        products=Product.objects.all().filter(is_available=True)
        paginator=Paginator(products,per_page=2)

    context={
        # 'paginator': paginator,
        'products': products,
    }

    return render(request,'store/store.html', context)

def product_detail(request,category_slug=None,product_slug=None):
    
    try:
        product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e 

    context={
        'product':product,
    }
    print(product.name)
    return render(request,'store/product_detail.html',context)