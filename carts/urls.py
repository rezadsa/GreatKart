from django.urls import path
from . import views

urlpatterns =[
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('sub_cart/<int:cartItem_id>/',views.sub_cart,name='sub_cart'),
    path('increase_cart/<int:cartItem_id>/',views.increase_cart,name='increase_cart'),
    path('remove_cartItem/<int:cartItem_id>/',views.remove_cartItem,name='remove_cartItem'),
]