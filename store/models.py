from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
     name           =models.CharField(max_length=200,unique=True)
     slug           =models.SlugField(max_length=200,unique=True)
     description    =models.TextField(max_length=500,blank=True,null=True)
     price          =models.DecimalField(max_digits=6,decimal_places=2)  
     image          =models.ImageField(upload_to='photos/product')
     stock          =models.IntegerField()
     is_available   =models.BooleanField(default=True)
     
     category       =models.ForeignKey(Category,on_delete=models.CASCADE)

     created_date   = models.DateTimeField(auto_now_add=True)
     modified_date  = models.DateTimeField(auto_now=True)

     def __str__(self):
          return f'{self.category.name!r}({self.name},{self.price})'
     
     def get_url(self):
          return reverse('product_detail',args=[self.category.slug,self.slug])
