from django.urls import path
from . import views

urlpatterns=[
       path('payment/',views.payment,name='payment'),
       path('deleteOrder/<int:order_number>',views.deleteOrder,name='deleteOrder'),
]