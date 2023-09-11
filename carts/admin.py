from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_created')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','user','product','quantity','is_active')
    list_display_links = ('cart','user','product')

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)