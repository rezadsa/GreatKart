from django.contrib import admin
from .models import Order, OrderProduct, Payment

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=('user','payment','first_name','last_name','email','order_total','status','ip','is_ordered','created_at','updated_at')

class OrderProductAdmin(admin.ModelAdmin):
    list_display=('order','user','payment','product','variation','colour','size','quantity','product_price','ordered','created_at','updated_at')

class PaymentAdmin(admin.ModelAdmin):
    list_display=('user','method','amount','status','created_at')

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Payment,PaymentAdmin)
