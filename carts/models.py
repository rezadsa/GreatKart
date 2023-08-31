from django.db import models
from store.models import Product,Variation

# Create your models here.

class Cart(models.Model):
    cart_id         =models.CharField(max_length=100, blank=True)
    date_created    =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    cart            =models.ForeignKey(Cart,on_delete=models.CASCADE)
    product         =models.ForeignKey(Product,on_delete=models.CASCADE)
    variation       =models.ManyToManyField(Variation,blank=True)
    quantity        =models.IntegerField()
    is_active       = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cart},{self.product},{self.quantity}'